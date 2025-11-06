from contextlib import asynccontextmanager
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends, Header
from app.models import (
    JobCreate,
    JobPublic,
    JobList,
    ApplyPayload,
    ApplicationPublic,
    ApplicationUpdate,
    ApplicationWithCandidate,
)
from app.deps import enable_cors, verify_admin_api_key
from app.db import init_db, close_db, get_db, check_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(title="Netter ATS", lifespan=lifespan)
enable_cors(app)


@app.get("/health")
async def health():
    """Vérifie que l'API et la base de données fonctionnent."""
    db_status = await check_db_connection()
    return {"status": "ok", "db": db_status}


# ===== Routes Jobs (Admin) =====

@app.post("/api/jobs", response_model=JobPublic, dependencies=[Depends(verify_admin_api_key)])
async def create_job(job: JobCreate):
    """Crée une nouvelle offre d'emploi (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    """
                    INSERT INTO jobs (slug, title, description_md, location, department, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, slug, title, description_md, location, department, status, created_at
                    """,
                    (job.slug, job.title, job.description_md, job.location, job.department, job.status),
                )
                row = await cur.fetchone()
                await conn.commit()
                
                return JobPublic(
                    id=row[0],
                    slug=row[1],
                    title=row[2],
                    description_md=row[3],
                    location=row[4],
                    department=row[5],
                    status=row[6],
                    created_at=row[7],
                )
            except Exception as e:
                await conn.rollback()
                if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                    raise HTTPException(status_code=400, detail="Slug already exists")
                raise HTTPException(status_code=500, detail=f"Error creating job: {str(e)}")


@app.get("/api/jobs", response_model=list[JobList], dependencies=[Depends(verify_admin_api_key)])
async def list_jobs():
    """Liste toutes les offres d'emploi (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, slug, title, location, department, status, created_at
                FROM jobs
                ORDER BY created_at DESC
                """
            )
            rows = await cur.fetchall()
            
            return [
                JobList(
                    id=row[0],
                    slug=row[1],
                    title=row[2],
                    location=row[3],
                    department=row[4],
                    status=row[5],
                    created_at=row[6],
                )
                for row in rows
            ]


# ===== Routes Jobs (Public) =====

@app.get("/api/jobs/public", response_model=list[JobList])
async def list_public_jobs():
    """Liste toutes les offres d'emploi ouvertes (public)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, slug, title, location, department, status, created_at
                FROM jobs
                WHERE status = 'open'
                ORDER BY created_at DESC
                """
            )
            rows = await cur.fetchall()
            
            return [
                JobList(
                    id=row[0],
                    slug=row[1],
                    title=row[2],
                    location=row[3],
                    department=row[4],
                    status=row[5],
                    created_at=row[6],
                )
                for row in rows
            ]


@app.get("/api/jobs/{slug}", response_model=JobPublic)
async def get_job(slug: str):
    """Récupère une offre d'emploi par son slug (public)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, slug, title, description_md, location, department, status, created_at
                FROM jobs
                WHERE slug = %s AND status = 'open'
                """,
                (slug,),
            )
            row = await cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Job not found or closed")
            
            return JobPublic(
                id=row[0],
                slug=row[1],
                title=row[2],
                description_md=row[3],
                location=row[4],
                department=row[5],
                status=row[6],
                created_at=row[7],
            )


# ===== Routes Applications =====

@app.post("/api/jobs/{slug}/apply")
async def apply_to_job(slug: str, payload: ApplyPayload):
    """Postule à une offre d'emploi (public)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que l'offre existe et est ouverte
            await cur.execute(
                "SELECT id FROM jobs WHERE slug = %s AND status = 'open'",
                (slug,),
            )
            job_row = await cur.fetchone()
            if not job_row:
                raise HTTPException(status_code=404, detail="Job not found or closed")
            
            job_id = job_row[0]
            
            # UPSERT du candidat (insert ou update si existe déjà)
            await cur.execute(
                """
                INSERT INTO candidates (email, full_name, linkedin_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) 
                DO UPDATE SET 
                    full_name = EXCLUDED.full_name,
                    linkedin_url = COALESCE(EXCLUDED.linkedin_url, candidates.linkedin_url)
                RETURNING id
                """,
                (payload.email, payload.full_name, payload.linkedin_url),
            )
            candidate_row = await cur.fetchone()
            candidate_id = candidate_row[0]
            
            # Vérifier si une candidature existe déjà pour ce job et ce candidat
            await cur.execute(
                """
                SELECT id FROM applications
                WHERE job_id = %s AND candidate_id = %s
                """,
                (job_id, candidate_id),
            )
            existing = await cur.fetchone()
            
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="You have already applied to this job"
                )
            
            # Créer la candidature
            await cur.execute(
                """
                INSERT INTO applications (job_id, candidate_id, stage)
                VALUES (%s, %s, 'new')
                RETURNING id, stage
                """,
                (job_id, candidate_id),
            )
            app_row = await cur.fetchone()
            await conn.commit()
            
            return {
                "ok": True,
                "message": "Application received",
                "stage": app_row[1],
                "application_id": app_row[0],
            }


@app.get("/api/jobs/{job_id}/applications", response_model=list[ApplicationWithCandidate], dependencies=[Depends(verify_admin_api_key)])
async def get_job_applications(job_id: UUID):
    """Récupère toutes les candidatures pour une offre (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT 
                    a.id,
                    a.job_id,
                    a.candidate_id,
                    a.stage,
                    a.notes,
                    a.created_at,
                    a.created_at as updated_at,
                    c.full_name as candidate_name,
                    c.email as candidate_email,
                    c.linkedin_url as candidate_linkedin_url
                FROM applications a
                JOIN candidates c ON a.candidate_id = c.id
                WHERE a.job_id = %s
                ORDER BY a.created_at DESC
                """,
                (job_id,),
            )
            rows = await cur.fetchall()
            
            return [
                ApplicationWithCandidate(
                    id=row[0],
                    job_id=row[1],
                    candidate_id=row[2],
                    stage=row[3],
                    notes=row[4],
                    created_at=row[5],
                    updated_at=row[6],
                    candidate_name=row[7],
                    candidate_email=row[8],
                    candidate_linkedin_url=row[9],
                )
                for row in rows
            ]


@app.patch("/api/applications/{application_id}", response_model=ApplicationPublic, dependencies=[Depends(verify_admin_api_key)])
async def update_application(application_id: UUID, update: ApplicationUpdate):
    """Met à jour une candidature (stage et/ou notes) (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que la candidature existe
            await cur.execute(
                "SELECT id FROM applications WHERE id = %s",
                (application_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Application not found")
            
            # Construire la requête UPDATE dynamiquement
            updates = []
            values = []
            
            if update.stage is not None:
                updates.append("stage = %s")
                values.append(update.stage)
            
            if update.notes is not None:
                updates.append("notes = %s")
                values.append(update.notes)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            values.append(application_id)
            
            await cur.execute(
                f"""
                UPDATE applications
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING id, job_id, candidate_id, stage, notes, created_at
                """,
                values,
            )
            row = await cur.fetchone()
            await conn.commit()
            
            return ApplicationPublic(
                id=row[0],
                job_id=row[1],
                candidate_id=row[2],
                stage=row[3],
                notes=row[4],
                created_at=row[5],
                updated_at=row[5],  # Utiliser created_at comme updated_at temporairement
            )
