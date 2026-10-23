"""Builds the Time Diary prototype page: static, semantic HTML for the shell, the timeline's
day sections and the Add activity dialog. app.js draws activities into the timeline."""
import datetime as dt, html, sys

OUT = sys.argv[1]
START = dt.date(2026, 10, 19)
DAYS = 7
TODAY_I = 1   # simulated "today" = Tue 20 Oct

ICON = {
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'prev': '<path d="M15 6l-6 6 6 6"/>',
    'next': '<path d="M9 6l6 6-6 6"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'close': '<path d="M6 6l12 12M18 6L6 18"/>',
    'lock': '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'pencil': '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
}
def icon(name, size=None):
    st = f' style="width:{size}px;height:{size}px"' if size else ''
    return f'<svg class="td-icon" viewBox="0 0 24 24" aria-hidden="true"{st}>{ICON[name]}</svg>'
def hm(q):
    m = (q % 96) * 15
    return f'{m // 60:02d}:{m % 60:02d}'
def day(i): return START + dt.timedelta(days=i)
def label(d): return f'{d:%a} {d.day} {d:%b}'
e = html.escape

# The catalogue, as the participant sees it. Modelled on the real pilot study (7 categories, 61 codes),
# so the list is as long as it will be in production. Categories still to confirm are left out.
CATALOGUE = [
    ('General & daily living', [
        ('general.sleeping', 'Sleeping', '', 'general', 'none', []),
        ('general.resting', 'Resting', 'Lunch break, couch time, downtime, …', 'general', 'none', []),
        ('general.adl', 'Activities of Daily Living', 'Eating, drinking, personal care, household routines, …', 'general', 'none', []),
        ('general.eating', 'Eating & drinking', '', 'general', 'none', []),
        ('general.care', 'Personal care & grooming', '', 'general', 'none', []),
    ]),
    ('Work & study', [
        ('work.paid', 'Paid work', 'Main job, self-employment, …', 'work', 'none', []),
        ('work.school', 'School', '', 'work', 'options', [
            ('primary', 'School: primary'), ('lower-secondary', 'School: lower secondary'),
            ('upper-secondary', 'School: upper secondary / Gymnasium')]),
        ('work.university', 'University', '', 'work', 'options', [
            ('bachelor', 'University: Bachelor'), ('master', 'University: Master'), ('phd', 'University: PhD')]),
        ('work.courses', 'Other courses / training', '', 'work', 'none', []),
        ('work.apprenticeship', 'Apprenticeship / vocational training', '', 'work', 'none', []),
        ('work.seminar', 'Further education seminar', '', 'work', 'none', []),
        ('work.homework', 'Homework & studying', '', 'work', 'none', []),
        ('work.meetings', 'Meetings', '', 'work', 'none', []),
        ('work.volunteering', 'Volunteering', '', 'work', 'none', []),
        ('work.jobsearch', 'Job seeking', '', 'work', 'none', []),
    ]),
    ('Travel & transit', [
        ('travel.travelling', 'Travelling', 'Walking, cycle, running, car, public transport, …', 'travel', 'options', [
            ('walking', 'Travelling: walking'), ('cycle', 'Travelling: cycle'), ('running', 'Travelling: running'),
            ('private-vehicle', 'Travelling: car, motorbike, moped, E-scooter, taxi or similar'),
            ('public-transport', 'Travelling: public transport'), ('other', 'Travelling: other')]),
        ('travel.commuting', 'Commuting to work or school', '', 'travel', 'none', []),
        ('travel.waiting', 'Waiting / transferring', '', 'travel', 'none', []),
    ]),
    ('Sport & physical activity', [
        ('sport.outdoors', 'Sport & exercise (outdoors)', 'Cycling, team sport, running outside, …', 'out', 'none', []),
        ('sport.gym', 'Sport in a gym or studio', 'Fitness studio, courses, …', 'out', 'none', []),
        ('sport.indoors', 'Sport indoors', 'Swimming, indoor courses, …', 'out', 'none', []),
        ('sport.walking', 'Walking for exercise', '', 'out', 'none', []),
        ('sport.cycling', 'Cycling for exercise', '', 'out', 'none', []),
        ('sport.team', 'Team sport', '', 'out', 'none', []),
        ('sport.home', 'Sport & exercise at home', 'Home workout, yoga, …', 'home', 'none', []),
    ]),
    ('Household & care', [
        ('home.cooking', 'Cooking & preparing food', '', 'home', 'none', []),
        ('home.cleaning', 'Cleaning & tidying', '', 'home', 'none', []),
        ('home.laundry', 'Laundry & ironing', '', 'home', 'none', []),
        ('home.repairs', 'Repairs & maintenance', '', 'home', 'none', []),
        ('home.gardening', 'Gardening', '', 'home', 'none', []),
        ('home.pets', 'Caring for pets', '', 'home', 'none', []),
        ('home.care-children', 'Caring for children', 'Feeding, playing, helping, …', 'home', 'none', []),
        ('home.care-adults', 'Caring for other adults', '', 'home', 'none', []),
        ('home.activities', 'Activities at home', 'Tidying up, organising, …', 'home', 'none', []),
    ]),
    ('Social, leisure & hobbies', [
        ('out.activities', 'Activities outside home', '', 'out', 'none', []),
        ('out.socialising', 'Meeting family or friends', 'Visiting, going out together, …', 'out', 'none', []),
        ('out.religion', 'Religious / spiritual practice, meditation', '', 'out', 'none', []),
        ('out.reading', 'Reading (paper book, magazine, newspaper)', '', 'out', 'none', []),
        ('out.hobby', 'Leisure / hobby (please specify)', '', 'out', 'text', []),
        ('out.culture', 'Cultural activity / event', 'Cinema, theatre, concert, museum, …', 'out', 'none', []),
        ('out.music', 'Playing or making music', '', 'out', 'none', []),
        ('out.games', 'Games & puzzles', 'Board games, cards, …', 'out', 'none', []),
    ]),
    ('Digital media', [
        ('digital.streaming', 'Video streaming', 'TV programmes, YouTube, …', 'digital', 'none', []),
        ('digital.calls', 'Social contact by phone or video call', 'Phone, Zoom, FaceTime, …', 'digital', 'none', []),
        ('digital.social-media', 'Social media', '', 'digital', 'none', []),
        ('digital.scrolling', 'Scrolling / consuming content', '', 'digital', 'none', []),
        ('digital.networking', 'Building networks / engaging with posts', '', 'digital', 'none', []),
        ('digital.messenger', 'Messenger / chatting', '', 'digital', 'none', []),
        ('digital.gaming', 'Gaming', '', 'digital', 'options', [
            ('console-alone', 'Gaming: console, alone'), ('console-together', 'Gaming: console, with others'),
            ('computer-alone', 'Gaming: computer, alone'), ('computer-together', 'Gaming: computer, with others'),
            ('mobile-alone', 'Gaming: mobile, alone'), ('mobile-together', 'Gaming: mobile, with others')]),
        ('digital.audio', 'Listening to audio', 'Music, podcasts, audiobooks, …', 'digital', 'none', []),
        ('digital.learning', 'Online learning', 'Duolingo, online courses, …', 'digital', 'none', []),
        ('digital.reading', 'Reading digitally', 'News, e-books, articles, …', 'digital', 'none', []),
        ('digital.browsing', 'Web browsing / life admin', '', 'digital', 'none', []),
        ('digital.shopping', 'Online shopping', '', 'digital', 'none', []),
        ('digital.editing', 'Photo & video editing', '', 'digital', 'none', []),
    ]),
    ('Other', [
        ('other.other', 'Other Activity', 'Please specify.', 'other', 'text', []),
        ('other.forgot', 'Forgot / Unspecified', '', 'other', 'none', []),
    ]),
]

def activity_button(a):
    aid, title, hint, pat, kind, opts = a
    end = {'options': icon('next'), 'text': icon('pencil'), 'none': ''}[kind]
    hint_html = f'<span class="td-activity__hint">{e(hint)}</span>' if hint else ''
    return (f'<li><button class="td-activity" type="button" data-activity-id="{aid}" data-redcap-field="" data-redcap-code="" '
            f'data-title="{e(title)}" data-pattern="{pat}" data-kind="{kind}">'
            f'<span class="td-pat td-pat--{pat}" aria-hidden="true"></span>'
            f'<span class="td-activity__body"><span class="td-activity__title">{e(title)}</span>{hint_html}</span>'
            + (f'<span class="td-activity__end">{end}</span>' if end else '') + '</button></li>')

groups = ''.join(
    f'<section class="td-activity-group" aria-labelledby="g-{k}"><h3 id="g-{k}">{e(cat)}</h3><ul>'
    + ''.join(activity_button(a) for a in acts) + '</ul></section>'
    for k, (cat, acts) in enumerate(CATALOGUE))

option_sets = ''.join(
    f'<fieldset class="td-options" data-for="{aid}" hidden><legend>Select an option for “{e(title)}”</legend>'
    + ''.join(f'<label class="td-option" data-activity-id="{aid}.{oid}" data-redcap-field="" data-redcap-code="">'
              f'<input type="radio" name="option" value="{aid}.{oid}" data-label="{e(ol)}"> {e(ol)}</label>' for oid, ol in opts)
    + '</fieldset>'
    for cat, acts in CATALOGUE for aid, title, hint, pat, kind, opts in acts if kind == 'options')

day_options = ''.join(f'<option value="{i}">{label(day(i))}</option>' for i in range(DAYS))
start_options = ''.join(f'<option value="{q}">{hm(q)}</option>' for q in range(96))
chips = ''.join(
    f'<label class="td-day-chip"><input type="checkbox" name="days" value="{i}" aria-label="{label(day(i))}">'
    f'<span class="td-day-chip__wd" aria-hidden="true">{day(i):%a}</span><span class="td-day-chip__d" aria-hidden="true">{day(i).day}</span></label>'
    for i in range(DAYS))

hours = ''.join(f'<li><time>{h:02d}:00</time></li>' for h in range(24))
days_html = ''.join(f'''
    <section class="td-tl-day" id="day-{day(i).isoformat()}" aria-labelledby="h-{i}" data-label="{label(day(i))}" data-index="{i}">
      <h2 class="td-tl-day__head" id="h-{i}">{label(day(i))}</h2>
      <div class="td-tl-grid">
        <ol class="td-tl-hours" aria-hidden="true">{hours}</ol>
        <ol class="td-tl-track" aria-label="Activities on {label(day(i))}"></ol>
      </div>
    </section>''' for i in range(DAYS))

rail_html = ''.join(
    f'<li><a class="td-rail__row" href="#day-{day(i).isoformat()}">'
    f'<span class="td-rail__day">{label(day(i))}</span>'
    f'<span class="td-rail__min" data-min>–</span>'
    f'<span class="td-rail__bar"><span class="td-rail__fill"></span></span>'
    f'</a></li>' for i in range(DAYS))

end = day(DAYS - 1)
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)">
<title>Time Diary</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
<style>
  :root {{ --topbar-h: calc(121px + env(safe-area-inset-top)); }}
  html {{ scroll-padding-top: var(--topbar-h); }}
  .td-app {{ max-width: var(--content-max); margin: 0 auto; }}

  /* Desktop shell (prototype only). Layout, not component styling: the phone layout above stays
     exactly as it is, and everything here is additive behind the 1200px query. */
  .td-topbar__note, .td-rail, .td-dock__idle {{ display: none; }}
  @media (min-width: 1200px) {{
    .td-app {{ max-width: 1360px; margin: 0 auto; display: grid; padding-top: var(--topbar-h);
      grid-template-columns: 260px minmax(0, 1fr) 380px; align-items: start; }}
    /* Header spans the shell and stays put. Fixed rather than sticky, as on phones: one paint path,
       no dependence on how a browser constrains sticky grid items. */
    .td-topbar {{ position: fixed; inset-inline: 0; margin-inline: auto; max-width: 1360px; }}
    .td-topbar__note {{ display: block; margin: 0; font-size: 0.875rem; line-height: 1.25rem;
      color: var(--ink-muted); white-space: nowrap; }}
    .td-daynav {{ display: none; }}
    .td-topbar ~ .td-timeline {{ padding-top: 0; }}

    .td-rail {{ display: block; grid-column: 1; grid-row: 2; position: sticky; top: var(--topbar-h);
      height: calc(100dvh - var(--topbar-h)); overflow: auto;
      padding: var(--space-4) var(--space-3) var(--space-6) var(--space-4);
      border-inline-end: 1px solid var(--line); }}
    .td-rail__title {{ margin: 0 0 var(--space-2); font-size: 0.75rem; line-height: 1rem; font-weight: 500;
      color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.04em; }}
    .td-rail__list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: var(--space-1); }}
    .td-rail__row {{ display: grid; grid-template-columns: 1fr auto; gap: var(--space-1) var(--space-2);
      padding: var(--space-2) var(--space-3); border: 1.5px solid transparent; border-radius: var(--radius-md);
      color: var(--ink); text-decoration: none; }}
    .td-rail__row:hover {{ background: var(--surface-100); }}
    .td-rail__row:focus-visible {{ outline: 3px solid var(--focus); outline-offset: 2px; }}
    .td-rail__row[aria-current="true"] {{ border-color: var(--ink); }}
    .td-rail__day {{ font-weight: 600; }}
    .td-rail__min {{ font-family: var(--font-mono); font-size: 0.8125rem; color: var(--ink-muted); }}
    .td-rail__bar {{ grid-column: 1 / -1; display: block; height: 6px; border-radius: var(--radius-pill);
      background: var(--surface-200); overflow: hidden; }}
    .td-rail__fill {{ display: block; height: 100%; width: var(--fill, 0); background: var(--ink); }}
    .td-rail__note {{ margin: var(--space-4) 0 0; font-size: 0.75rem; line-height: 1.125rem;
      color: var(--ink-muted); }}

    /* The timeline is the only long column; its day heading sticks under the header so the day
       you are in stays named while you scroll. */
    .td-timeline {{ grid-column: 2; grid-row: 2; padding-bottom: var(--space-8); }}
    .td-tl-day__head {{ position: sticky; top: var(--topbar-h); z-index: 1; }}

    /* The Add activity dialog docks into the third column instead of covering the calendar. */
    .td-dock__idle {{ grid-column: 3; grid-row: 2; position: sticky; top: var(--topbar-h);
      height: calc(100dvh - var(--topbar-h)); display: grid; align-content: start; gap: var(--space-3);
      padding: var(--space-5) var(--space-4); border-inline-start: 1px solid var(--line); }}
    .td-dock__idle p {{ margin: 0; }}
    .td-dock__idle-text {{ font-size: 0.875rem; line-height: 1.375rem; color: var(--ink-muted); }}
    .td-dock__idle:has(+ #add[open]) {{ display: none; }}
    #add {{ grid-column: 3; grid-row: 2; position: sticky; top: var(--topbar-h);
      height: calc(100dvh - var(--topbar-h)); max-height: none;
      border-inline-start: 1px solid var(--line); }}
    /* A docked panel is not modal, so the page behind it keeps scrolling. */
    html:has(#add[open]) {{ overflow: auto; }}
    #fab {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="td-app">
  <header class="td-topbar" id="topbar">
    <div class="td-topbar__row">
      <button class="td-icon-btn" type="button" popovertarget="menu" aria-label="Menu">{icon('menu')}</button>
      <div class="td-topbar__title"><h1 class="td-topbar__name">Time Diary</h1></div>
      <p class="td-topbar__note">Desktop layout prototype · {DAYS} days · sample data</p>
      <button class="td-btn td-btn--secondary td-btn--sm" type="button" id="submit-btn" aria-disabled="true" popovertarget="submit-why">{icon('lock')} Submit</button>
    </div>
    <nav class="td-daynav" aria-label="Day">
      <a class="td-icon-btn" id="day-prev" href="#day-{day(TODAY_I - 1).isoformat()}" aria-label="Previous day">{icon('prev')}</a>
      <div class="td-daynav__label">
        <p class="td-daynav__day" id="day-label">{label(day(TODAY_I))}</p>
        <p class="td-daynav__meta" id="day-meta">Day {TODAY_I + 1} of {DAYS}</p>
      </div>
      <a class="td-icon-btn" id="day-next" href="#day-{day(TODAY_I + 1).isoformat()}" aria-label="Next day">{icon('next')}</a>
    </nav>
  </header>

  <aside class="td-rail" aria-label="Days and coverage">
    <h2 class="td-rail__title">Days</h2>
    <ol class="td-rail__list">{rail_html}</ol>
    <p class="td-rail__note">Placeholder panel. The minutes and bars are the real coverage; what is still open is
      what belongs here besides the days (submission state, the submit button).</p>
  </aside>
  <main class="td-timeline" id="timeline">
    <div class="td-notice td-timeline__notice" id="empty-note" role="status" hidden>
      <svg class="td-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>
      <div class="td-notice__body"><p id="empty-text"></p></div>
    </div>
    <div class="td-notice td-notice--readonly td-timeline__notice" id="readonly-note" role="note" hidden>
      <svg class="td-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>
      <div class="td-notice__body"><p id="readonly-text"></p></div>
    </div>
    <div class="td-notice td-timeline__notice" id="storage-warning" role="status" hidden>
      <div class="td-notice__body"><p>This browser isn't letting the app save on this phone. Activities you add will be lost when you close it.</p></div>
    </div>
    <div id="days"></div>
  </main>
<div class="td-dock__idle">
  <p class="td-dock__idle-title">Activity list</p>
  <p class="td-dock__idle-text">The activities appear here, in the same column as the form, so the calendar stays in
    view while you add something.</p>
  <button class="td-btn td-btn--primary" type="button" id="dock-add">Add activity</button>
</div>
<dialog class="td-modal" id="add" aria-labelledby="add-title">
  <form id="add-form" method="post" action="#" novalidate>
    <div class="td-modal__head">
      <button class="td-icon-btn" type="button" id="add-back" aria-label="Back to activities" hidden>{icon('prev')}</button>
      <h2 id="add-title" tabindex="-1"><span class="td-modal__step" id="add-step">Step 1 of 2</span><span class="td-vh">: </span><span id="add-heading">Add activity</span></h2>
      <span class="td-modal__count" id="add-count" hidden></span>
      <button class="td-icon-btn" type="button" id="add-close" aria-label="Close">{icon('close')}</button>
    </div>

    <div class="td-modal__body" id="step-1">
      <div class="td-activity-list">
        <section class="td-activity-group" id="recent-group" aria-labelledby="g-recent" hidden>
          <h3 id="g-recent">Used recently</h3>
          <ul id="recent-list"></ul>
        </section>
        {groups}
      </div>
    </div>

    <div class="td-modal__body" id="step-2" hidden>
      <div class="td-chosen"><span class="td-pat" id="chosen-pat" aria-hidden="true"></span><span class="td-chosen__text" id="chosen-text"></span></div>
      {option_sets}
      <div class="td-field" id="note-field" hidden>
        <label for="note">What did you do?</label>
        <input class="td-input" id="note" name="note" maxlength="200" autocomplete="off">
      </div>
      <fieldset class="td-time-range">
        <legend>When?</legend>
        <div class="td-field"><label for="f-day">Day</label><select class="td-select td-select--text" id="f-day" name="day"></select></div>
        <div class="td-time-range__row">
          <div class="td-field"><label for="f-start">Start</label><select class="td-select" id="f-start" name="start">{start_options}</select></div>
          <div class="td-field"><label for="f-end">End</label><select class="td-select" id="f-end" name="end" aria-describedby="end-hint"></select></div>
        </div>
        <p class="td-duration">Lasts <output id="f-dur" for="f-start f-end"></output></p>
        <p class="td-hint" id="end-hint" hidden></p>
      </fieldset>
      <fieldset class="td-days" id="f-days-set" aria-describedby="days-hint">
        <legend>Also on other days?</legend>
        <p class="td-hint" id="days-hint">Same activity and time. Tap the days that were the same.</p>
        <div class="td-days__grid" id="f-chips"></div>
      </fieldset>
      <div class="td-notice td-notice--attention" id="add-error" tabindex="-1" hidden>
        <div class="td-notice__body"><p class="td-notice__title" id="add-error-title"></p><p id="add-error-text"></p></div>
      </div>
    </div>

    <div class="td-modal__foot" id="add-foot" hidden>
      <button class="td-btn td-btn--primary td-btn--block" type="submit" name="then" value="close" id="add-btn">Add to timeline</button>
      <button class="td-btn td-btn--secondary td-btn--block" type="submit" name="then" value="next" id="next-btn">Save and add another</button>
      <button class="td-btn td-btn--primary td-btn--block" type="submit" name="then" value="save" id="save-btn" hidden>Save changes</button>
      <button class="td-btn td-btn--secondary td-btn--block" type="button" id="delete-btn" hidden>Delete activity</button>
    </div>
  </form>

  <div popover id="discard" class="td-popover td-popover--sheet" role="alertdialog" aria-labelledby="discard-title" aria-describedby="discard-text">
    <h2 id="discard-title">Discard this activity?</h2>
    <p id="discard-text">It hasn't been added to your timeline yet.</p>
    <div class="td-popover__stack">
      <button class="td-btn td-btn--primary td-btn--block" type="button" id="keep-editing" autofocus>Keep editing</button>
      <button class="td-btn td-btn--secondary td-btn--block" type="button" id="discard-go">Discard</button>
    </div>
  </div>
</dialog>
</div>


<div class="td-pages" id="pages" hidden>
  <section class="td-page" id="page-waiting" aria-labelledby="pt-waiting" hidden>
    <header class="td-page__head">
      <button class="td-icon-btn" type="button" popovertarget="menu" aria-label="Menu">{icon('menu')}</button>
      <p class="td-topbar__name">Time Diary</p>
    </header>
    <main class="td-confirm td-waiting">
      <h1 id="pt-waiting" tabindex="-1">Your next diary starts on <span id="wait-date"></span></h1>
      <p id="wait-days"></p>
    </main>
  </section>

  <section class="td-page" id="page-help" aria-labelledby="pt-help" hidden>
    <header class="td-page__head"><a class="td-icon-btn" href="#timeline" aria-label="Back to your diary">{icon('prev')}</a><h1 id="pt-help" tabindex="-1">How to add an activity</h1></header>
    <main class="td-page__body td-prose">
      <ol>
        <li><strong>Tap Add activity</strong> at the bottom of the screen, or tap a “Nothing added” gap on the timeline.</li>
        <li><strong>Choose what you did.</strong> Pick it from the list. Things you chose before are at the top.</li>
        <li><strong>Say more, if asked.</strong> For example, how you travelled.</li>
        <li><strong>Set the day and the time</strong> it started and ended. Times go in 15-minute steps. An activity can end the next day, like sleep.</li>
        <li><strong>Tap Add to timeline.</strong> To add more in one go, tap Save and add another.</li>
      </ol>
      <p>Can't remember? Choose <strong>Forgot / Unspecified</strong>. To change or remove an activity, tap it on the timeline.</p>
      <p>When every day has activities, tap <strong>Submit</strong> at the top to check your diary and send it to the research team.</p>
    </main>
  </section>

  <section class="td-page" id="page-study" aria-labelledby="pt-study" hidden>
    <header class="td-page__head"><a class="td-icon-btn" href="#timeline" aria-label="Back to your diary">{icon('prev')}</a><h1 id="pt-study" tabindex="-1">Study information</h1></header>
    <main class="td-page__body td-prose">
      <p class="td-placeholder">The research team's description of the study goes here: what it is about, who runs it, how long it lasts, and how the diaries are used.</p>
    </main>
  </section>

  <section class="td-page" id="page-privacy" aria-labelledby="pt-privacy" hidden>
    <header class="td-page__head"><a class="td-icon-btn" href="#timeline" aria-label="Back to your diary">{icon('prev')}</a><h1 id="pt-privacy" tabindex="-1">Data protection</h1></header>
    <main class="td-page__body td-prose">
      <p>The activities you add are saved on this phone straight away, even without an internet connection.</p>
      <p>They stay on this phone until you submit your diary. When the research team confirms they received it, you see a thank-you screen with a reference.</p>
      <p>After that, the diary is locked: you can look at it, but not change it.</p>
      <p class="td-placeholder">The research team's data protection statement goes here: who is responsible for the data, how it is stored and for how long, and your rights.</p>
    </main>
  </section>

  <section class="td-page" id="page-contact" aria-labelledby="pt-contact" hidden>
    <header class="td-page__head"><a class="td-icon-btn" href="#timeline" aria-label="Back to your diary">{icon('prev')}</a><h1 id="pt-contact" tabindex="-1">Contact</h1></header>
    <main class="td-page__body td-prose">
      <p>Questions about the study or the app, or using a new phone? Contact the research team.</p>
      <dl class="td-facts">
        <dt>Email</dt><dd class="td-placeholder">research team email</dd>
        <dt>Phone</dt><dd class="td-placeholder">research team phone number</dd>
        <dt>Your participant code</dt><dd class="td-placeholder">participant code</dd>
      </dl>
    </main>
  </section>
</div>

<button class="td-fab" type="button" id="fab">{icon('plus')} Add activity</button>

<div popover id="submit-why" class="td-popover" role="dialog" aria-labelledby="sw-title">
  <h2 id="sw-title">Not ready to submit yet</h2>
  <p id="sw-text">Submit opens when every day from {label(START)} to {label(end)} has activities.</p>
  <div class="td-popover__actions">
    <a class="td-btn td-btn--primary td-btn--sm" id="sw-go" href="#timeline">Go to the first empty day</a>
    <button class="td-btn td-btn--ghost td-btn--sm" type="button" popovertarget="submit-why" popovertargetaction="hide">Close</button>
  </div>
</div>

<nav popover id="menu" class="td-drawer" aria-labelledby="menu-title">
  <div class="td-drawer__head">
    <h2 id="menu-title">Menu</h2>
    <button class="td-icon-btn" type="button" popovertarget="menu" popovertargetaction="hide" aria-label="Close menu">{icon('close')}</button>
  </div>
  <ul aria-label="Actions">
    <li><a class="td-drawer__item" href="#help" data-view="help">How to add an activity</a></li>
  </ul>
  <hr>
  <ul aria-label="Pages">
    <li><a class="td-drawer__item" href="#study" data-view="study">Study information</a></li>
    <li><a class="td-drawer__item" href="#privacy" data-view="privacy">Data protection</a></li>
    <li><a class="td-drawer__item" href="#contact" data-view="contact">Contact</a></li>
  </ul>
  <hr>
  <ul aria-label="Prototype">
    <li><button class="td-drawer__item" type="button" id="fill-days">Fill empty days <span class="td-drawer__meta">prototype</span></button></li>
    <li><button class="td-drawer__item" type="button" id="skip-next">Skip to the next diary <span class="td-drawer__meta">prototype</span></button></li>
    <li><button class="td-drawer__item" type="button" id="pretend-offline"><span id="pretend-offline-label">Pretend to be offline</span> <span class="td-drawer__meta">prototype</span></button></li>
    <li><button class="td-drawer__item" type="button" id="reset-data">Reset to sample data <span class="td-drawer__meta">prototype</span></button></li>
  </ul>
</nav>
<dialog class="td-modal" id="review" aria-labelledby="review-title">
  <form id="review-form" method="post" action="#" novalidate>
    <div class="td-modal__head">
      <button class="td-icon-btn" type="button" id="review-back" aria-label="Back to your diary">{icon('prev')}</button>
    </div>
    <div class="td-modal__body td-modal__body--flush">
      <div class="td-page-head"><h1 id="review-title" tabindex="-1">Check your diary</h1><p id="review-period"></p></div>
      <div class="td-review" id="review-list"></div>
    </div>
    <footer class="td-sticky-foot">
      <button class="td-btn td-btn--primary td-btn--block" type="button" popovertarget="confirm-submit">Submit diary</button>
      <p>You'll confirm on the next step before anything is sent.</p>
    </footer>
    <div popover id="confirm-submit" class="td-popover td-popover--sheet" role="dialog" aria-labelledby="cs-title" aria-describedby="cs-text">
      <h2 id="cs-title">Submit your diary?</h2>
      <p id="cs-text"></p>
      <div class="td-popover__stack">
        <button class="td-btn td-btn--primary td-btn--block" type="submit" id="cs-yes">Yes, submit</button>
        <button class="td-btn td-btn--secondary td-btn--block" type="button" popovertarget="confirm-submit" popovertargetaction="hide" autofocus>Not yet, keep checking</button>
      </div>
    </div>
  </form>
</dialog>

<dialog class="td-modal" id="thanks" aria-labelledby="thanks-title">
  <div class="td-confirm td-confirm--fill">
    <div class="td-confirm__mark" aria-hidden="true"><svg class="td-icon" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
    <h1 id="thanks-title" tabindex="-1">Thank you</h1>
    <p id="thanks-sent"></p>
    <p id="thanks-next-date"></p>
    <p class="td-confirm__receipt" id="thanks-receipt"></p>
  </div>
  <footer class="td-sticky-foot">
    <button class="td-btn td-btn--primary td-btn--block" type="button" id="thanks-next">Start next diary</button>
  </footer>
</dialog>

<p class="td-vh" id="live" role="status"></p>
<div popover="manual" id="toast" class="td-toast">
  <p class="td-toast__text" id="toast-text"></p>
  <button class="td-toast__action" type="button" id="toast-undo">Undo</button>
</div>

<script src="app.js"></script>
</body>
</html>
'''
open(OUT, 'w').write(page)
print('wrote', OUT, len(page), 'bytes')
