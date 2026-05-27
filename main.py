from typing import Optional
from nicegui import ui, app as nicegui_app

try:
    from .auth import authenticate_user, create_user, get_user_by_username
    from .db import create_db_and_tables, get_session
    from .models import User, Visibility
    from .pdf_export import generate_pdf
    from .services import (
        create_card, create_card_set, delete_card, delete_card_set,
        get_card_set, get_card_set_statistics, get_user_statistics,
        grant_permission, list_card_sets_for_user, list_cards_in_set,
        list_public_card_sets, record_answer, update_card, update_card_set,
    )
except ImportError:
    try:
        from app.auth import authenticate_user, create_user, get_user_by_username
        from app.db import create_db_and_tables, get_session
        from app.models import User, Visibility
        from app.pdf_export import generate_pdf
        from app.services import (
            create_card, create_card_set, delete_card, delete_card_set,
            get_card_set, get_card_set_statistics, get_user_statistics,
            grant_permission, list_card_sets_for_user, list_cards_in_set,
            list_public_card_sets, record_answer, update_card, update_card_set,
        )
    except ImportError:
        from auth import authenticate_user, create_user, get_user_by_username
        from db import create_db_and_tables, get_session
        from models import User, Visibility
        from pdf_export import generate_pdf
        from services import (
            create_card, create_card_set, delete_card, delete_card_set,
            get_card_set, get_card_set_statistics, get_user_statistics,
            grant_permission, list_card_sets_for_user, list_cards_in_set,
            list_public_card_sets, record_answer, update_card, update_card_set,
        )

create_db_and_tables()

PRIMARY   = '#FFB800'
PRIMARY_L = '#FFF9E6'
BG        = '#F5F6FA'
CARD_BG   = '#FFFFFF'
TEXT      = '#111827'
MUTED     = '#6B7280'
BORDER    = '#E5E7EB'
SUCCESS   = '#22C55E'
DANGER    = '#EF4444'


def get_user() -> Optional[User]:
    uid = nicegui_app.storage.user.get('user_id')
    if not uid:
        return None
    with get_session() as s:
        return s.get(User, uid)


def set_user(u: Optional[User]) -> None:
    nicegui_app.storage.user['user_id'] = u.id if u else None


def _seed() -> None:
    with get_session() as s:
        if not get_user_by_username(s, 'demo'):
            create_user(s, 'demo', 'demo@example.com', 'demo123')
    if not list_public_card_sets():
        try:
            from .seed_data import populate_database_with_sample_cards
        except ImportError:
            try:
                from app.seed_data import populate_database_with_sample_cards
            except ImportError:
                from seed_data import populate_database_with_sample_cards
        populate_database_with_sample_cards()


_seed()


def _nav_bar() -> None:
    u = get_user()
    with ui.header().style(
        f'background:{CARD_BG};border-bottom:3px solid {PRIMARY};'
        'box-shadow:0 2px 8px rgba(0,0,0,0.08)'
    ):
        with ui.row().classes('w-full items-center justify-between px-8 py-3'):
            ui.label('FlashLearn').classes('text-xl font-bold').style(f'color:{PRIMARY}')
            if u:
                with ui.row().classes('gap-1 items-center'):
                    ui.label(f'Benutzer: {u.username}').classes('text-sm mr-3').style(f'color:{MUTED}')
                    ui.button('Dashboard', on_click=lambda: ui.navigate.to('/')).props('flat dense').style(f'color:{TEXT}')
                    ui.button('Lernen', on_click=lambda: ui.navigate.to('/learn')).props('flat dense').style(f'color:{TEXT}')
                    ui.button('Statistik', on_click=lambda: ui.navigate.to('/stats')).props('flat dense').style(f'color:{TEXT}')
                    ui.button('Abmelden', on_click=lambda: (set_user(None), ui.navigate.to('/login'))).props('flat dense').style(f'color:{DANGER}')


def _set_card(cs, u: User, editable: bool) -> None:
    cards = list_cards_in_set(cs.id)
    vis_text = 'Privat' if str(cs.visibility) in ('private', 'Visibility.PRIVATE') else 'Oeffentlich'
    with ui.card().classes('p-5').style(
        f'background:{CARD_BG};border:1px solid {BORDER};'
        f'border-left:5px solid {PRIMARY};'
        'box-shadow:0 2px 8px rgba(0,0,0,0.06)'
    ):
        ui.label(cs.name).classes('font-bold text-lg').style(f'color:{TEXT}')
        if cs.description:
            ui.label(cs.description).classes('text-sm mt-1').style(f'color:{MUTED}')
        with ui.row().classes('items-center gap-2 mt-3'):
            ui.label(f'{len(cards)} Karten').classes('text-sm').style(
                f'background:{PRIMARY_L};color:{TEXT};padding:2px 10px;border-radius:12px'
            )
            ui.label(vis_text).classes('text-xs').style(f'color:{MUTED}')
        with ui.row().classes('gap-2 mt-4 flex-wrap'):
            ui.button('Lernen', on_click=lambda sid=cs.id: ui.navigate.to(f'/learn/{sid}')).style(
                f'background:{PRIMARY};color:black;font-weight:600'
            ).props('dense')
            if editable:
                ui.button('Karten', on_click=lambda sid=cs.id: ui.navigate.to(f'/cards/{sid}')).props('flat dense').style(f'color:{TEXT}')
                ui.button('Bearbeiten', on_click=lambda sid=cs.id: ui.navigate.to(f'/edit-set/{sid}')).props('flat dense').style(f'color:{TEXT}')
                ui.button('PDF', on_click=lambda sid=cs.id: _export_pdf(sid)).props('flat dense').style(f'color:{TEXT}')
                ui.button('Loeschen', on_click=lambda sid=cs.id: _delete_set(sid)).props('flat dense').style(f'color:{DANGER}')


@ui.page('/login')
def login_page():
    if get_user():
        ui.navigate.to('/')
        return
    ui.query('body').style(f'background:{BG}')
    with ui.column().classes('w-full h-screen items-center justify-center gap-3'):
        ui.label('FlashLearn').classes('text-4xl font-bold').style(f'color:{PRIMARY}')
        ui.label('Lerne effizienter mit Karteikarten').classes('text-sm mb-4').style(f'color:{MUTED}')
        with ui.card().classes('w-96 p-6').style(
            f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
            'box-shadow:0 4px 24px rgba(0,0,0,0.10)'
        ):
            ui.label('Anmelden').classes('text-2xl font-bold mb-2').style(f'color:{TEXT}')
            un = ui.input('Benutzername').classes('w-full')
            pw = ui.input('Passwort', password=True).classes('w-full')
            err = ui.label('').style(f'color:{DANGER}')

            def do_login():
                with get_session() as s:
                    u = authenticate_user(s, un.value, pw.value)
                    if u:
                        set_user(u)
                        ui.navigate.to('/')
                    else:
                        err.set_text('Ungueltige Anmeldedaten')

            ui.button('Anmelden', on_click=lambda: do_login()).classes('w-full mt-2').style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )
            with ui.row().classes('w-full justify-center mt-2'):
                ui.label('Noch kein Konto?').classes('text-sm').style(f'color:{MUTED}')
                ui.button('Registrieren', on_click=lambda: ui.navigate.to('/register')).props('flat dense').style(f'color:{PRIMARY}')


@ui.page('/register')
def register_page():
    if get_user():
        ui.navigate.to('/')
        return
    ui.query('body').style(f'background:{BG}')
    with ui.column().classes('w-full h-screen items-center justify-center gap-3'):
        ui.label('FlashLearn').classes('text-4xl font-bold').style(f'color:{PRIMARY}')
        with ui.card().classes('w-96 p-6').style(
            f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
            'box-shadow:0 4px 24px rgba(0,0,0,0.10)'
        ):
            ui.label('Konto erstellen').classes('text-2xl font-bold mb-2').style(f'color:{TEXT}')
            un  = ui.input('Benutzername').classes('w-full')
            em  = ui.input('E-Mail').classes('w-full')
            pw  = ui.input('Passwort', password=True).classes('w-full')
            pw2 = ui.input('Passwort wiederholen', password=True).classes('w-full')
            err = ui.label('').style(f'color:{DANGER}')

            def do_register():
                if not un.value.strip():
                    err.set_text('Benutzername darf nicht leer sein')
                    return
                if pw.value != pw2.value:
                    err.set_text('Passwoerter stimmen nicht ueberein')
                    return
                if len(pw.value) < 6:
                    err.set_text('Passwort muss mindestens 6 Zeichen haben')
                    return
                with get_session() as s:
                    if get_user_by_username(s, un.value):
                        err.set_text('Benutzername bereits vergeben')
                        return
                    try:
                        u = create_user(s, un.value.strip(), em.value, pw.value)
                        set_user(u)
                        ui.navigate.to('/')
                    except Exception as exc:
                        err.set_text(str(exc)[:60])

            ui.button('Konto erstellen', on_click=lambda: do_register()).classes('w-full mt-2').style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )
            with ui.row().classes('w-full justify-center mt-2'):
                ui.label('Bereits ein Konto?').classes('text-sm').style(f'color:{MUTED}')
                ui.button('Anmelden', on_click=lambda: ui.navigate.to('/login')).props('flat dense').style(f'color:{PRIMARY}')


@ui.page('/')
def dashboard_page():
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    stats    = get_user_statistics(u.id)
    my_sets  = list_card_sets_for_user(u.id)
    all_pub  = list_public_card_sets()
    pub_sets = [s for s in all_pub if s.creator_id != u.id]
    with ui.column().classes('max-w-6xl mx-auto w-full px-6 py-8 gap-6'):
        ui.label(f'Willkommen zurueck, {u.username}!').classes('text-3xl font-bold').style(f'color:{TEXT}')
        with ui.row().classes('w-full gap-4 flex-wrap'):
            for label, value, accent in [
                ('Beantwortet', stats['total_answers'],       TEXT),
                ('Richtig',     stats['correct'],             SUCCESS),
                ('Falsch',      stats['incorrect'],           DANGER),
                ('Genauigkeit', f"{stats['accuracy']:.0f}%", PRIMARY),
                ('Meine Sets',  len(my_sets),                 PRIMARY),
            ]:
                with ui.card().classes('flex-1 p-5 text-center').style(
                    f'background:{CARD_BG};border-top:4px solid {accent};'
                    'box-shadow:0 2px 8px rgba(0,0,0,0.06);min-width:110px'
                ):
                    ui.label(str(value)).classes('text-3xl font-bold').style(f'color:{accent}')
                    ui.label(label).classes('text-xs mt-1').style(f'color:{MUTED}')
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Meine Sets').classes('text-2xl font-bold').style(f'color:{TEXT}')
            ui.button('+ Neues Set', on_click=lambda: ui.navigate.to('/new-set')).style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )
        if not my_sets:
            with ui.card().classes('w-full p-10 text-center').style(
                f'background:{CARD_BG};border:2px dashed {BORDER}'
            ):
                ui.label('Noch keine eigenen Sets').classes('text-lg font-semibold mt-2').style(f'color:{MUTED}')
                ui.label('Erstelle dein erstes Set oder nutze die oeffentlichen Sets unten.').classes('text-sm').style(f'color:{MUTED}')
        else:
            with ui.grid(columns=3).classes('w-full gap-4'):
                for cs in my_sets:
                    _set_card(cs, u, editable=True)
        if pub_sets:
            ui.separator()
            ui.label('Oeffentliche Lernsets').classes('text-2xl font-bold').style(f'color:{TEXT}')
            with ui.grid(columns=3).classes('w-full gap-4'):
                for cs in pub_sets:
                    _set_card(cs, u, editable=False)


def _export_pdf(set_id: int) -> None:
    cs = get_card_set(set_id)
    if not cs:
        return
    cards = list_cards_in_set(set_id)
    buf = generate_pdf(cs, cards)
    ui.download(buf.getvalue(), filename=f'{cs.name}.pdf')


def _delete_set(set_id: int) -> None:
    u = get_user()
    if not u:
        return
    cs = get_card_set(set_id)
    if cs and cs.creator_id == u.id:
        delete_card_set(set_id)
        ui.notify('Set geloescht', type='positive')
        ui.navigate.to('/')


@ui.page('/new-set')
def new_set_page():
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    with ui.column().classes('max-w-2xl mx-auto w-full px-6 py-8 gap-4'):
        with ui.row().classes('items-center gap-3'):
            ui.button('Zurueck', on_click=lambda: ui.navigate.to('/')).props('flat').style(f'color:{PRIMARY}')
            ui.label('Neues Set erstellen').classes('text-2xl font-bold').style(f'color:{TEXT}')
        with ui.card().classes('w-full p-6').style(
            f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
            'box-shadow:0 4px 16px rgba(0,0,0,0.08)'
        ):
            name_in = ui.input('Set-Name').classes('w-full')
            desc_in = ui.textarea('Beschreibung (optional)').classes('w-full')
            vis_in  = ui.select(
                options={'private': 'Privat', 'public': 'Oeffentlich'},
                label='Sichtbarkeit',
                value='private',
            ).classes('w-full')
            err = ui.label('').style(f'color:{DANGER}')

            def do_create():
                if not name_in.value.strip():
                    err.set_text('Bitte einen Namen eingeben')
                    return
                cs = create_card_set(
                    creator_id=u.id,
                    name=name_in.value.strip(),
                    description=desc_in.value,
                    visibility=vis_in.value,
                )
                ui.notify('Set erstellt!', type='positive')
                ui.navigate.to(f'/cards/{cs.id}')

            ui.button('Set erstellen', on_click=lambda: do_create()).classes('mt-2').style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )


@ui.page('/edit-set/{set_id}')
def edit_set_page(set_id: int):
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    cs = get_card_set(set_id)
    if not cs or cs.creator_id != u.id:
        ui.navigate.to('/')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    with ui.column().classes('max-w-2xl mx-auto w-full px-6 py-8 gap-4'):
        with ui.row().classes('items-center gap-3'):
            ui.button('Zurueck', on_click=lambda: ui.navigate.to('/')).props('flat').style(f'color:{PRIMARY}')
            ui.label('Set bearbeiten').classes('text-2xl font-bold').style(f'color:{TEXT}')
        with ui.card().classes('w-full p-6').style(
            f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
            'box-shadow:0 4px 16px rgba(0,0,0,0.08)'
        ):
            current_vis = 'public' if str(cs.visibility) not in ('private', 'Visibility.PRIVATE') else 'private'
            name_in = ui.input('Set-Name', value=cs.name).classes('w-full')
            desc_in = ui.textarea('Beschreibung', value=cs.description or '').classes('w-full')
            vis_in  = ui.select(
                options={'private': 'Privat', 'public': 'Oeffentlich'},
                label='Sichtbarkeit',
                value=current_vis,
            ).classes('w-full')
            err = ui.label('').style(f'color:{DANGER}')

            def do_save():
                if not name_in.value.strip():
                    err.set_text('Bitte einen Namen eingeben')
                    return
                update_card_set(
                    set_id=set_id,
                    name=name_in.value.strip(),
                    description=desc_in.value,
                    visibility=vis_in.value,
                )
                ui.notify('Set aktualisiert!', type='positive')
                ui.navigate.to('/')

            ui.button('Speichern', on_click=lambda: do_save()).classes('mt-2').style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )


@ui.page('/cards/{set_id}')
def cards_page(set_id: int):
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    cs = get_card_set(set_id)
    if not cs:
        ui.navigate.to('/')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    editable = (cs.creator_id == u.id)
    with ui.column().classes('max-w-4xl mx-auto w-full px-6 py-8 gap-5'):
        with ui.row().classes('items-center gap-3 flex-wrap'):
            ui.button('Zurueck', on_click=lambda: ui.navigate.to('/')).props('flat').style(f'color:{PRIMARY}')
            ui.label(cs.name).classes('text-2xl font-bold').style(f'color:{TEXT}')
        if editable:
            with ui.card().classes('w-full p-6').style(
                f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
                'box-shadow:0 2px 8px rgba(0,0,0,0.06)'
            ):
                ui.label('Neue Karte hinzufuegen').classes('font-bold text-lg mb-2').style(f'color:{TEXT}')
                with ui.row().classes('w-full gap-3'):
                    front_in = ui.input('Vorderseite (Frage)').classes('flex-1')
                    back_in  = ui.input('Rueckseite (Antwort)').classes('flex-1')

                def do_add():
                    if not front_in.value or not back_in.value:
                        ui.notify('Bitte beide Felder ausfullen', type='negative')
                        return
                    create_card(set_id, front_in.value, back_in.value)
                    ui.notify('Karte hinzugefuegt!', type='positive')
                    ui.navigate.to(f'/cards/{set_id}')

                ui.button('Karte hinzufuegen', on_click=lambda: do_add()).style(
                    f'background:{PRIMARY};color:black;font-weight:700'
                )
        cards = list_cards_in_set(set_id)
        with ui.row().classes('items-center justify-between'):
            ui.label(f'{len(cards)} Karten').classes('text-xl font-bold').style(f'color:{TEXT}')
            ui.button('Lernen', on_click=lambda: ui.navigate.to(f'/learn/{set_id}')).style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )
        if not cards:
            with ui.card().classes('w-full p-10 text-center').style(
                f'background:{CARD_BG};border:2px dashed {BORDER}'
            ):
                ui.label('Noch keine Karten in diesem Set.').style(f'color:{MUTED}')
        else:
            with ui.grid(columns=2).classes('w-full gap-3'):
                for card in cards:
                    with ui.card().classes('p-4').style(
                        f'background:{CARD_BG};border:1px solid {BORDER};border-left:4px solid {PRIMARY}'
                    ):
                        ui.label(card.front).classes('font-semibold').style(f'color:{TEXT}')
                        ui.separator()
                        ui.label(card.back).classes('text-sm mt-1').style(f'color:{MUTED}')
                        if editable:
                            with ui.row().classes('gap-1 mt-1'):
                                ui.button(
                                    'Bearbeiten',
                                    on_click=lambda cid=card.id, cf=card.front, cb=card.back: _open_edit_card(cid, set_id, cf, cb),
                                ).props('flat dense').style(f'color:{TEXT}')
                                ui.button(
                                    'Loeschen',
                                    on_click=lambda cid=card.id: _delete_card(set_id, cid),
                                ).props('flat dense').style(f'color:{DANGER}')
        if editable:
            ui.separator()
            with ui.card().classes('w-full p-6').style(
                f'background:{CARD_BG};border-top:4px solid {PRIMARY};'
                'box-shadow:0 2px 8px rgba(0,0,0,0.06)'
            ):
                ui.label('Set teilen').classes('font-bold text-lg mb-2').style(f'color:{TEXT}')
                ui.label('Benutzername eingeben, um Zugriff zu gewaehren:').classes('text-sm mb-3').style(f'color:{MUTED}')
                with ui.row().classes('w-full gap-3 items-end'):
                    share_un   = ui.input('Benutzername').classes('flex-1')
                    share_perm = ui.select(
                        options={'view': 'Anschauen', 'edit': 'Bearbeiten'},
                        label='Berechtigung',
                        value='view',
                    ).classes('w-48')
                share_err = ui.label('').style(f'color:{DANGER}')

                def do_share():
                    if not share_un.value.strip():
                        share_err.set_text('Bitte einen Benutzernamen eingeben')
                        return
                    with get_session() as s:
                        target = get_user_by_username(s, share_un.value.strip())
                    if not target:
                        share_err.set_text('Benutzer nicht gefunden')
                        return
                    if target.id == u.id:
                        share_err.set_text('Du kannst das Set nicht mit dir selbst teilen')
                        return
                    grant_permission(set_id, target.id, share_perm.value)
                    ui.notify(f'Set mit {target.username} geteilt!', type='positive')
                    share_err.set_text('')
                    share_un.set_value('')

                ui.button('Teilen', on_click=lambda: do_share()).style(
                    f'background:{PRIMARY};color:black;font-weight:700'
                )


def _open_edit_card(card_id: int, set_id: int, current_front: str, current_back: str) -> None:
    with ui.dialog() as dialog, ui.card().classes('p-6 w-96').style(
        f'background:{CARD_BG};border-top:4px solid {PRIMARY}'
    ):
        ui.label('Karte bearbeiten').classes('text-xl font-bold mb-4').style(f'color:{TEXT}')
        front_in = ui.input('Vorderseite (Frage)', value=current_front).classes('w-full')
        back_in  = ui.input('Rueckseite (Antwort)', value=current_back).classes('w-full')
        err = ui.label('').style(f'color:{DANGER}')

        def do_save():
            if not front_in.value.strip() or not back_in.value.strip():
                err.set_text('Beide Felder sind erforderlich')
                return
            update_card(card_id, front_in.value.strip(), back_in.value.strip())
            ui.notify('Karte aktualisiert!', type='positive')
            dialog.close()
            ui.navigate.to(f'/cards/{set_id}')

        with ui.row().classes('gap-2 mt-4'):
            ui.button('Speichern', on_click=lambda: do_save()).style(
                f'background:{PRIMARY};color:black;font-weight:700'
            )
            ui.button('Abbrechen', on_click=dialog.close).props('flat').style(f'color:{MUTED}')
    dialog.open()


def _delete_card(set_id: int, card_id: int) -> None:
    delete_card(card_id)
    ui.notify('Karte geloescht', type='positive')
    ui.navigate.to(f'/cards/{set_id}')


@ui.page('/learn/{set_id}')
def learn_set_page(set_id: int):
    _learn_ui(preselected_set_id=set_id)


@ui.page('/learn')
def learn_page():
    _learn_ui(preselected_set_id=None)


def _learn_ui(preselected_set_id: Optional[int]) -> None:
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    my_sets  = list_card_sets_for_user(u.id)
    pub_sets = list_public_card_sets()
    all_sets = list({s.id: s for s in my_sets + pub_sets}.values())
    if not all_sets:
        with ui.column().classes('max-w-3xl mx-auto p-6'):
            ui.label('Keine Sets verfuegbar').classes('text-2xl').style(f'color:{MUTED}')
        return
    current_cards: list = []
    idx     = [0]
    flipped = [False]
    options     = {str(cs.id): cs.name for cs in all_sets}
    default_val = str(preselected_set_id) if preselected_set_id else str(all_sets[0].id)
    with ui.column().classes('max-w-3xl mx-auto w-full px-6 py-8 gap-5'):
        ui.label('Lernmodus').classes('text-3xl font-bold').style(f'color:{TEXT}')
        ui.button('Zurueck', on_click=lambda: ui.navigate.to('/')).props('flat').style(f'color:{PRIMARY}')
        set_sel      = ui.select(options=options, label='Set auswaehlen', value=default_val).classes('w-full')
        progress_bar = ui.linear_progress(value=0).classes('w-full').style(f'color:{PRIMARY}')
        with ui.card().classes('w-full p-12 text-center').style(
            f'background:{CARD_BG};border:2px solid {BORDER};min-height:260px;'
            'border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,0.10);cursor:pointer'
        ) as card_el:
            side_lbl     = ui.label('FRAGE').classes('text-xs font-bold tracking-widest').style(f'color:{PRIMARY}')
            card_lbl     = ui.label('Klicke Starten um zu beginnen').classes('text-2xl font-semibold mt-4').style(f'color:{TEXT}')
            progress_lbl = ui.label('').classes('text-sm mt-6').style(f'color:{MUTED}')
        with ui.row().classes('w-full justify-center gap-4'):
            ui.button('Starten', on_click=lambda: start()).style(f'background:{PRIMARY};color:black;font-weight:700')
            ui.button('Umdrehen', on_click=lambda: flip()).props('outline').style(f'color:{PRIMARY};border-color:{PRIMARY}')
        with ui.row().classes('w-full justify-center gap-6'):
            ui.button('Falsch', on_click=lambda: answer(False)).style(
                f'background:#FEE2E2;color:{DANGER};font-weight:700;min-width:140px'
            )
            ui.button('Richtig', on_click=lambda: answer(True)).style(
                f'background:#DCFCE7;color:{SUCCESS};font-weight:700;min-width:140px'
            )

        def update() -> None:
            if not current_cards:
                return
            card = current_cards[idx[0]]
            if flipped[0]:
                side_lbl.set_text('ANTWORT')
                card_lbl.set_text(card.back)
                card_el.style(
                    f'background:{PRIMARY_L};border:2px solid {PRIMARY};min-height:260px;'
                    'border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,0.10);cursor:pointer'
                )
            else:
                side_lbl.set_text('FRAGE')
                card_lbl.set_text(card.front)
                card_el.style(
                    f'background:{CARD_BG};border:2px solid {BORDER};min-height:260px;'
                    'border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,0.10);cursor:pointer'
                )
            progress_lbl.set_text(f'Karte {idx[0] + 1} von {len(current_cards)}')
            progress_bar.set_value((idx[0] + 1) / len(current_cards))

        def start() -> None:
            current_cards[:] = list_cards_in_set(int(set_sel.value))
            idx[0]     = 0
            flipped[0] = False
            if not current_cards:
                ui.notify('Dieses Set hat noch keine Karten', type='warning')
                return
            update()

        def flip() -> None:
            if not current_cards:
                return
            flipped[0] = not flipped[0]
            update()

        def answer(correct: bool) -> None:
            if not current_cards:
                return
            record_answer(u.id, current_cards[idx[0]].id, correct)
            idx[0]     = (idx[0] + 1) % len(current_cards)
            flipped[0] = False
            if idx[0] == 0:
                ui.notify('Alle Karten durchgearbeitet!', type='positive')
            update()

        card_el.on('click', lambda: flip())
        if preselected_set_id:
            start()


@ui.page('/stats')
def stats_page():
    u = get_user()
    if not u:
        ui.navigate.to('/login')
        return
    ui.query('body').style(f'background:{BG}')
    _nav_bar()
    stats   = get_user_statistics(u.id)
    my_sets = list_card_sets_for_user(u.id)
    with ui.column().classes('max-w-5xl mx-auto w-full px-6 py-8 gap-6'):
        with ui.row().classes('items-center gap-3'):
            ui.button('Zurueck', on_click=lambda: ui.navigate.to('/')).props('flat').style(f'color:{PRIMARY}')
            ui.label('Meine Statistik').classes('text-3xl font-bold').style(f'color:{TEXT}')
        with ui.row().classes('w-full gap-4 flex-wrap'):
            for title, value, accent in [
                ('Beantwortet', stats['total_answers'],       TEXT),
                ('Richtig',     stats['correct'],             SUCCESS),
                ('Falsch',      stats['incorrect'],           DANGER),
                ('Genauigkeit', f"{stats['accuracy']:.1f}%", PRIMARY),
            ]:
                with ui.card().classes('flex-1 p-6 text-center').style(
                    f'background:{CARD_BG};border-top:4px solid {accent};'
                    'box-shadow:0 2px 8px rgba(0,0,0,0.06);min-width:140px'
                ):
                    ui.label(str(value)).classes('text-4xl font-bold').style(f'color:{accent}')
                    ui.label(title).classes('text-sm mt-1').style(f'color:{MUTED}')
        if my_sets:
            ui.label('Fortschritt nach Set').classes('text-xl font-bold').style(f'color:{TEXT}')
            for cs in my_sets:
                ss  = get_card_set_statistics(cs.id, u.id)
                pct = ss['accuracy'] / 100
                with ui.card().classes('w-full p-5').style(
                    f'background:{CARD_BG};border:1px solid {BORDER};border-left:4px solid {PRIMARY};'
                    'box-shadow:0 2px 8px rgba(0,0,0,0.04)'
                ):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label(cs.name).classes('font-bold').style(f'color:{TEXT}')
                        ui.label(f"{ss['accuracy']:.1f}%").classes('font-bold').style(f'color:{PRIMARY}')
                    ui.label(
                        f"Gemeistert: {ss['cards_mastered']} / {ss['total_cards']} Karten"
                    ).classes('text-sm mt-1').style(f'color:{MUTED}')
                    ui.linear_progress(value=pct).classes('mt-2').style(f'color:{PRIMARY}')
        else:
            with ui.card().classes('w-full p-10 text-center').style(
                f'background:{CARD_BG};border:2px dashed {BORDER}'
            ):
                ui.label('Noch keine Lernaktivitaet vorhanden.').style(f'color:{MUTED}')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='FlashLearn', host='0.0.0.0', port=8080,
           storage_secret='flashlearn-secret-key-2024', favicon='')
