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
    ApplicationNoteCreate,
    ApplicationNote,
    EmailTemplateCreate,
    EmailTemplateUpdate,
    EmailTemplate,
    EmailSend,
    Email,
    CandidateWithApplications,
)
from app.deps import enable_cors, verify_admin_api_key
from app.db import init_db, close_db, get_db, check_db_connection
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Import Resend conditionnellement
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    print("⚠️  Resend non installé. Les fonctionnalités email seront désactivées.")
    print("   Pour activer: pip install resend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(title="Netter ATS", lifespan=lifespan)
enable_cors(app)

# Initialize Resend (si disponible)
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
RESEND_FROM_NAME = os.getenv("RESEND_FROM_NAME", "Netter ATS")

if RESEND_AVAILABLE and RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    print(f"✅ Resend configuré - Emails envoyés depuis: {RESEND_FROM_EMAIL}")
elif RESEND_AVAILABLE and not RESEND_API_KEY:
    print("⚠️  RESEND_API_KEY non configurée. Les emails ne pourront pas être envoyés.")
    print("   Configurez RESEND_API_KEY dans votre fichier .env")
elif not RESEND_AVAILABLE:
    print("⚠️  Resend non installé. Installez-le avec: pip install resend")


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


@app.get("/api/jobs/{job_id}", response_model=JobPublic, dependencies=[Depends(verify_admin_api_key)])
async def get_job_by_id(job_id: UUID):
    """Récupère une offre d'emploi par son ID (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, slug, title, description_md, location, department, status, created_at
                FROM jobs
                WHERE id = %s
                """,
                (job_id,),
            )
            row = await cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Job not found")
            
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


@app.delete("/api/jobs/{job_id}", dependencies=[Depends(verify_admin_api_key)])
async def delete_job(job_id: UUID):
    """Supprime une offre d'emploi (admin uniquement). Les candidatures associées seront supprimées automatiquement."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que l'offre existe
            await cur.execute(
                """
                SELECT id FROM jobs WHERE id = %s
                """,
                (job_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Job not found")
            
            # Supprimer l'offre (les candidatures seront supprimées automatiquement via CASCADE)
            await cur.execute(
                """
                DELETE FROM jobs WHERE id = %s
                """,
                (job_id,),
            )
            await conn.commit()
            
            return {"message": "Job deleted successfully"}


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


@app.post("/api/applications/{application_id}/notes", response_model=ApplicationNote, dependencies=[Depends(verify_admin_api_key)])
async def create_application_note(application_id: UUID, note: ApplicationNoteCreate):
    """Crée une note pour une candidature (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que la candidature existe
            await cur.execute(
                "SELECT id FROM applications WHERE id = %s",
                (application_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Application not found")
            
            # Insérer la note
            try:
                await cur.execute(
                    """
                    INSERT INTO application_notes (application_id, stage, report, rating, interviewer)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, application_id, stage, report, rating, interviewer, created_at, updated_at
                    """,
                    (application_id, note.stage, note.report, note.rating, note.interviewer),
                )
                row = await cur.fetchone()
                await conn.commit()
            except Exception as e:
                if 'does not exist' in str(e) or 'relation "application_notes" does not exist' in str(e):
                    raise HTTPException(
                        status_code=500,
                        detail="La table application_notes n'existe pas. Veuillez exécuter la migration SQL (migration_add_notes_table.sql) dans Supabase."
                    )
                raise
            
            return ApplicationNote(
                id=row[0],
                application_id=row[1],
                stage=row[2],
                report=row[3],
                rating=row[4],
                interviewer=row[5],
                created_at=row[6],
                updated_at=row[7],
            )


@app.get("/api/applications/{application_id}/notes", response_model=list[ApplicationNote], dependencies=[Depends(verify_admin_api_key)])
async def get_application_notes(application_id: UUID):
    """Récupère toutes les notes d'une candidature (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que la candidature existe
            await cur.execute(
                "SELECT id FROM applications WHERE id = %s",
                (application_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Application not found")
            
            # Récupérer les notes
            try:
                await cur.execute(
                    """
                    SELECT id, application_id, stage, report, rating, interviewer, created_at, updated_at
                    FROM application_notes
                    WHERE application_id = %s
                    ORDER BY created_at DESC
                    """,
                    (application_id,),
                )
                rows = await cur.fetchall()
            except Exception as e:
                if 'does not exist' in str(e) or 'relation "application_notes" does not exist' in str(e):
                    # Si la table n'existe pas, retourner une liste vide au lieu d'une erreur
                    # pour permettre au frontend de fonctionner même sans migration
                    return []
                raise
            
            return [
                ApplicationNote(
                    id=row[0],
                    application_id=row[1],
                    stage=row[2],
                    report=row[3],
                    rating=row[4],
                    interviewer=row[5],
                    created_at=row[6],
                    updated_at=row[7],
                )
                for row in rows
            ]


# ===== Routes Email Templates =====

@app.get("/api/email-templates", response_model=list[EmailTemplate], dependencies=[Depends(verify_admin_api_key)])
async def list_email_templates():
    """Liste tous les templates d'email (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, name, subject, body, created_at, updated_at
                FROM email_templates
                ORDER BY created_at DESC
                """
            )
            rows = await cur.fetchall()
            
            return [
                EmailTemplate(
                    id=row[0],
                    name=row[1],
                    subject=row[2],
                    body=row[3],
                    created_at=row[4],
                    updated_at=row[5],
                )
                for row in rows
            ]


@app.post("/api/email-templates", response_model=EmailTemplate, dependencies=[Depends(verify_admin_api_key)])
async def create_email_template(template: EmailTemplateCreate):
    """Crée un nouveau template d'email (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO email_templates (name, subject, body)
                VALUES (%s, %s, %s)
                RETURNING id, name, subject, body, created_at, updated_at
                """,
                (template.name, template.subject, template.body),
            )
            row = await cur.fetchone()
            await conn.commit()
            
            return EmailTemplate(
                id=row[0],
                name=row[1],
                subject=row[2],
                body=row[3],
                created_at=row[4],
                updated_at=row[5],
            )


@app.get("/api/email-templates/{template_id}", response_model=EmailTemplate, dependencies=[Depends(verify_admin_api_key)])
async def get_email_template(template_id: int):
    """Récupère un template d'email par son ID (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, name, subject, body, created_at, updated_at
                FROM email_templates
                WHERE id = %s
                """,
                (template_id,),
            )
            row = await cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Template not found")
            
            return EmailTemplate(
                id=row[0],
                name=row[1],
                subject=row[2],
                body=row[3],
                created_at=row[4],
                updated_at=row[5],
            )


@app.patch("/api/email-templates/{template_id}", response_model=EmailTemplate, dependencies=[Depends(verify_admin_api_key)])
async def update_email_template(template_id: int, update: EmailTemplateUpdate):
    """Met à jour un template d'email (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que le template existe
            await cur.execute(
                "SELECT id FROM email_templates WHERE id = %s",
                (template_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Template not found")
            
            # Construire la requête de mise à jour
            updates = []
            values = []
            
            if update.name is not None:
                updates.append("name = %s")
                values.append(update.name)
            if update.subject is not None:
                updates.append("subject = %s")
                values.append(update.subject)
            if update.body is not None:
                updates.append("body = %s")
                values.append(update.body)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            updates.append("updated_at = NOW()")
            values.append(template_id)
            
            await cur.execute(
                f"""
                UPDATE email_templates
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING id, name, subject, body, created_at, updated_at
                """,
                values,
            )
            row = await cur.fetchone()
            await conn.commit()
            
            return EmailTemplate(
                id=row[0],
                name=row[1],
                subject=row[2],
                body=row[3],
                created_at=row[4],
                updated_at=row[5],
            )


@app.delete("/api/email-templates/{template_id}", dependencies=[Depends(verify_admin_api_key)])
async def delete_email_template(template_id: int):
    """Supprime un template d'email (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "DELETE FROM email_templates WHERE id = %s RETURNING id",
                (template_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Template not found")
            await conn.commit()
            
            return {"message": "Template deleted successfully"}


# ===== Routes Emails =====

def replace_template_variables(text: str, candidate_name: str) -> str:
    """Remplace les variables dans le template (ex: {{candidate_name}})."""
    return text.replace("{{candidate_name}}", candidate_name)


@app.post("/api/emails/send", response_model=Email, dependencies=[Depends(verify_admin_api_key)])
async def send_email(email_data: EmailSend):
    """Envoie un email à un candidat via Resend (admin uniquement)."""
    if not RESEND_AVAILABLE:
        raise HTTPException(status_code=500, detail="Resend n'est pas installé. Installez-le avec: pip install resend")
    if not RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Resend API key not configured")
    
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Récupérer les informations du candidat
            await cur.execute(
                """
                SELECT id, email, full_name
                FROM candidates
                WHERE id = %s
                """,
                (email_data.candidate_id,),
            )
            candidate_row = await cur.fetchone()
            
            if not candidate_row:
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            candidate_email = candidate_row[1]
            candidate_name = candidate_row[2]
            
            # Remplacer les variables dans le sujet et le corps
            subject = replace_template_variables(email_data.subject, candidate_name)
            body = replace_template_variables(email_data.body, candidate_name)
            
            # Envoyer l'email via Resend
            try:
                # Utiliser l'email de base Resend pour les tests (format recommandé par Resend)
                from_email = RESEND_FROM_EMAIL if RESEND_FROM_EMAIL else "onboarding@resend.dev"
                from_name = RESEND_FROM_NAME if RESEND_FROM_NAME else "Netter ATS"
                
                # En mode test Resend, on ne peut envoyer qu'à l'email du compte
                # Pour les tests, utiliser samuel@netterai.com (email du compte Resend)
                # En production avec domaine vérifié, utiliser candidate_email
                test_email = os.getenv("RESEND_TEST_EMAIL", "samuel@netterai.com")
                recipient_email = test_email  # Utiliser l'email de test pour l'instant
                
                # Format exact recommandé par Resend
                params = {
                    "from": f"{from_name} <{from_email}>",
                    "to": [recipient_email],  # Utiliser l'email de test
                    "subject": f"[TEST - Destinataire: {candidate_email}] {subject}",
                    "html": f"<p><strong>Email destiné à:</strong> {candidate_email}</p><p><strong>Nom:</strong> {candidate_name}</p><hr>{body.replace(chr(10), '<br>')}"
                }
                email_response = resend.Emails.send(params)
                
                # Enregistrer l'email dans la base de données
                sender_email = RESEND_FROM_EMAIL if RESEND_FROM_EMAIL else "onboarding@resend.dev"
                sender_name = RESEND_FROM_NAME if RESEND_FROM_NAME else "Netter ATS"
                
                await cur.execute(
                    """
                    INSERT INTO emails (candidate_id, subject, body, sender_email, sender_name, template_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, candidate_id, subject, body, sender_email, sender_name, template_id, created_at
                    """,
                    (
                        email_data.candidate_id,
                        subject,
                        body,
                        sender_email,
                        sender_name,
                        email_data.template_id,
                    ),
                )
                row = await cur.fetchone()
                await conn.commit()
                
                return Email(
                    id=row[0],
                    candidate_id=row[1],
                    subject=row[2],
                    body=row[3],
                    sender_email=row[4],
                    sender_name=row[5],
                    template_id=row[6],
                    created_at=row[7],
                )
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                error_msg = str(e)
                print(f"❌ Erreur lors de l'envoi d'email: {error_msg}")
                print(f"📋 Détails: {error_details}")
                
                # Message d'erreur plus clair pour les problèmes Resend courants
                if "only send testing emails to your own email address" in error_msg:
                    raise HTTPException(
                        status_code=400,
                        detail="Resend est en mode test. Vous devez vérifier un domaine dans Resend pour envoyer à d'autres adresses. Pour les tests, les emails sont envoyés à samuel@netterai.com."
                    )
                else:
                    raise HTTPException(status_code=500, detail=f"Failed to send email: {error_msg}")


@app.get("/api/candidates", response_model=list[CandidateWithApplications], dependencies=[Depends(verify_admin_api_key)])
async def get_all_candidates():
    """Récupère tous les candidats avec leurs candidatures (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Récupérer tous les candidats
            await cur.execute(
                """
                SELECT id, email, full_name, linkedin_url, created_at
                FROM candidates
                ORDER BY created_at DESC
                """
            )
            candidates_rows = await cur.fetchall()
            
            candidates = []
            for candidate_row in candidates_rows:
                candidate_id = candidate_row[0]
                
                # Récupérer les candidatures de ce candidat
                await cur.execute(
                    """
                    SELECT id, job_id, candidate_id, stage, notes, created_at
                    FROM applications
                    WHERE candidate_id = %s
                    ORDER BY created_at DESC
                    """,
                    (candidate_id,),
                )
                applications_rows = await cur.fetchall()
                
                applications = [
                    ApplicationPublic(
                        id=row[0],
                        job_id=row[1],
                        candidate_id=row[2],
                        stage=row[3],
                        notes=row[4],
                        created_at=row[5],
                        updated_at=row[5],  # Utiliser created_at si updated_at n'existe pas
                    )
                    for row in applications_rows
                ]
                
                candidates.append(
                    CandidateWithApplications(
                        id=candidate_id,
                        email=candidate_row[1],
                        full_name=candidate_row[2],
                        linkedin_url=candidate_row[3],
                        created_at=candidate_row[4],
                        updated_at=candidate_row[4],  # Utiliser created_at si updated_at n'existe pas
                        applications=applications,
                    )
                )
            
            return candidates


@app.delete("/api/candidates/{candidate_id}", dependencies=[Depends(verify_admin_api_key)])
async def delete_candidate(candidate_id: UUID):
    """Supprime un candidat (admin uniquement). Les candidatures associées seront supprimées automatiquement."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que le candidat existe
            await cur.execute(
                "SELECT id FROM candidates WHERE id = %s",
                (candidate_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            # Supprimer le candidat (les candidatures seront supprimées automatiquement via CASCADE)
            await cur.execute(
                "DELETE FROM candidates WHERE id = %s",
                (candidate_id,),
            )
            await conn.commit()
            
            return {"message": "Candidate deleted successfully"}


@app.get("/api/candidates/{candidate_id}/emails", response_model=list[Email], dependencies=[Depends(verify_admin_api_key)])
async def get_candidate_emails(candidate_id: UUID):
    """Récupère l'historique des emails d'un candidat (admin uniquement)."""
    async with get_db() as conn:
        async with conn.cursor() as cur:
            # Vérifier que le candidat existe
            await cur.execute(
                "SELECT id FROM candidates WHERE id = %s",
                (candidate_id,),
            )
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            # Récupérer les emails
            await cur.execute(
                """
                SELECT id, candidate_id, subject, body, sender_email, sender_name, template_id, created_at
                FROM emails
                WHERE candidate_id = %s
                ORDER BY created_at DESC
                """,
                (candidate_id,),
            )
            rows = await cur.fetchall()
            
            return [
                Email(
                    id=row[0],
                    candidate_id=row[1],
                    subject=row[2],
                    body=row[3],
                    sender_email=row[4],
                    sender_name=row[5],
                    template_id=row[6],
                    created_at=row[7],
                )
                for row in rows
            ]
