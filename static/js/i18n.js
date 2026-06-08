const TRANSLATIONS = {
  es: {
    confirm_completed: '¿Marcar "{name}" como completado? Se le quitará el rol activo si tenía uno.',
    toast_role_conflict: 'El rol {role} ya lo tiene "{name}"',
    metric_backlog: 'Juegos en backlog',
    metric_completed_total: 'Juegos completados',
    chart_completed_year: 'Completados por año',
    toast_duplicate: 'Ya existe un juego con ese nombre',
    field_completed_date: 'Fecha de completado',
    nav_home:'Inicio', nav_games:'Mis juegos', nav_stats:'Estadísticas', nav_settings:'Ajustes',
    page_home:'Inicio', page_games:'Mis juegos', page_stats:'Estadísticas', page_settings:'Ajustes',
    role_principal:'Principal', role_secundario:'Secundario', role_comodin:'Comodín', role_none:'Sin rol',
    status_playing:'Activo', status_backlog:'Backlog', status_paused:'Pausado', status_completed:'Completado', status_abandoned:'Abandonado',
    no_game:'Sin asignar', played_today:'✓ Jugado hoy', no_sessions:'Sin sesiones aún',
    day_ago:'Hace 1 día', days_ago:'Hace {n} días',
    day_week:'{n} día esta semana', days_week:'{n} días esta semana',
    btn_play:'▶ Jugar',
    metric_week:'Sesiones esta semana', metric_month:'Sesiones este mes', metric_top_role:'Rol más jugado',
    chart_title:'Días jugados por semana', most_played_title:'Más jugado',
    this_week:'Esta semana', this_month:'Este mes', this_week_label:'Esta sem.',
    completed_title:'Juegos completados', no_completed:'Aún no has completado ningún juego.',
    session_1:'1 sesión', sessions_n:'{n} sesiones',
    filter_all:'Todos', filter_active:'Activos', filter_backlog:'Backlog',
    filter_paused:'Pausados', filter_completed:'Completados', filter_abandoned:'Abandonados',
    no_games_msg:'No hay juegos en esta categoría.',
    btn_add:'+ Añadir juego', btn_edit:'Editar', btn_delete:'Eliminar',
    btn_cancel:'Cancelar', btn_save:'Guardar', btn_load:'Cargar', btn_loading:'Cargando...',
    modal_add:'Añadir juego', modal_edit:'Editar juego',
    hltb_label:'URL de HowLongToBeat (opcional)', hltb_ph:'https://howlongtobeat.com/game/...',
    hltb_ok:'✓ Datos cargados correctamente', hltb_err:'✗ No se pudo obtener el juego',
    field_name:'Nombre *', field_cover:'URL portada', field_genres:'Géneros (separados por coma)',
    field_platform:'Plataforma', field_status:'Estado', field_role:'Rol',
    name_required:'El nombre es obligatorio',
    confirm_delete:'¿Eliminar "{name}"? Esta acción no se puede deshacer.',
    setting_theme:'Tema', theme_standard:'Estándar', theme_dark:'Oscuro', theme_light:'Claro',
    setting_lang:'Idioma', setting_week:'Inicio de semana', monday:'Lunes', sunday:'Domingo',
    toast_played:'¡Sesión registrada!', toast_already:'Ya habías registrado una sesión hoy',
    toast_added:'Juego añadido', toast_updated:'Juego actualizado', toast_deleted:'Juego eliminado',
    toast_saved:'Ajuste guardado', toast_err_save:'Error al guardar', toast_err_delete:'Error al eliminar',
    sort_by: 'Ordenar por:', sort_name: 'Nombre',
    sort_platform: 'Plataforma', sort_added: 'Fecha añadido', sort_status: 'Estado',
  },
  en: {
    confirm_completed: 'Mark "{name}" as completed? Its active role will be removed if it had one.',
    toast_role_conflict: 'The {role} role is already assigned to "{name}"',
    metric_backlog: 'Games in backlog',
    metric_completed_total: 'Completed games',
    chart_completed_year: 'Completed per year',
    toast_duplicate: 'A game with that name already exists',
    field_completed_date: 'Completion date',
    nav_home:'Home', nav_games:'My games', nav_stats:'Statistics', nav_settings:'Settings',
    page_home:'Home', page_games:'My games', page_stats:'Statistics', page_settings:'Settings',
    role_principal:'Main', role_secundario:'Secondary', role_comodin:'Wildcard', role_none:'No role',
    status_playing:'Active', status_backlog:'Backlog', status_paused:'Paused', status_completed:'Completed', status_abandoned:'Abandoned',
    no_game:'Not assigned', played_today:'✓ Played today', no_sessions:'No sessions yet',
    day_ago:'1 day ago', days_ago:'{n} days ago',
    day_week:'{n} day this week', days_week:'{n} days this week',
    btn_play:'▶ Play',
    metric_week:'Sessions this week', metric_month:'Sessions this month', metric_top_role:'Most played role',
    chart_title:'Days played per week', most_played_title:'Most played',
    this_week:'This week', this_month:'This month', this_week_label:'This wk.',
    completed_title:'Completed games', no_completed:"You haven't completed any games yet.",
    session_1:'1 session', sessions_n:'{n} sessions',
    filter_all:'All', filter_active:'Active', filter_backlog:'Backlog',
    filter_paused:'Paused', filter_completed:'Completed', filter_abandoned:'Abandoned',
    no_games_msg:'No games in this category.',
    btn_add:'+ Add game', btn_edit:'Edit', btn_delete:'Delete',
    btn_cancel:'Cancel', btn_save:'Save', btn_load:'Load', btn_loading:'Loading...',
    modal_add:'Add game', modal_edit:'Edit game',
    hltb_label:'HowLongToBeat URL (optional)', hltb_ph:'https://howlongtobeat.com/game/...',
    hltb_ok:'✓ Data loaded successfully', hltb_err:'✗ Could not find the game',
    field_name:'Name *', field_cover:'Cover URL', field_genres:'Genres (comma separated)',
    field_platform:'Platform', field_status:'Status', field_role:'Role',
    name_required:'Name is required',
    confirm_delete:'Delete "{name}"? This action cannot be undone.',
    setting_theme:'Theme', theme_standard:'Standard', theme_dark:'Dark', theme_light:'Light',
    setting_lang:'Language', setting_week:'Week start', monday:'Monday', sunday:'Sunday',
    toast_played:'Session recorded!', toast_already:'You already recorded a session today',
    toast_added:'Game added', toast_updated:'Game updated', toast_deleted:'Game deleted',
    toast_saved:'Setting saved', toast_err_save:'Error saving', toast_err_delete:'Error deleting',
    sort_by: 'Sort by:', sort_name: 'Name',
    sort_platform: 'Platform', sort_added: 'Date added', sort_status: 'Status',
  }
};

let currentLang = localStorage.getItem('ab_lang') || 'es';

function t(key, params = {}) {
  const str = (TRANSLATIONS[currentLang] || TRANSLATIONS.es)[key] || key;
  return str.replace(/\{(\w+)\}/g, (_, k) => params[k] !== undefined ? params[k] : '{' + k + '}');
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => el.textContent = t(el.getAttribute('data-i18n')));
  document.querySelectorAll('[data-i18n-ph]').forEach(el => el.placeholder = t(el.getAttribute('data-i18n-ph')));
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('ab_lang', lang);
  document.documentElement.setAttribute('lang', lang);
  applyTranslations();
}

document.addEventListener('DOMContentLoaded', applyTranslations);