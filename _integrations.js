/**
 * LUCIVE 통합 헬퍼 · Klaviyo + GA4 + Zapier
 * ─────────────────────────────────────────────────────────────
 * 1) 아래 CONFIG 의 4개 값만 채우면 자동 동작
 * 2) 미설정 시 console.log 만 찍히고 페이지는 정상 동작 (mock-safe)
 * 3) 모든 함수는 비동기, 실패해도 페이지 흐름 차단 안 됨
 *
 * 사용:
 *   <script src="./_integrations.js"></script> 만 페이지에 추가하면
 *   window.LUCIVE_INTEGRATIONS 로 접근 가능 + GA4 자동 초기화
 */
window.LUCIVE_INTEGRATIONS = (function(){

  const CONFIG = {
    /* ─────────────── 채워주세요 ─────────────── */

    // Klaviyo Public API Key (Account → Settings → API Keys)
    // 형식: 6자 영숫자 (예: 'AbC123')
    // ⚠️ Private Key (pk_xxx...) 는 절대 여기 두지 마세요. 이 파일은 브라우저로 노출됩니다.
    KLAVIYO_PUBLIC_KEY: 'SUzTai',

    // Klaviyo List ID (Audience → Lists & Segments → 해당 리스트 → Settings)
    // 형식: 6자 영숫자 (예: 'XyZ789')
    KLAVIYO_LIST_ID: 'RPr3C5',

    // GA4 Measurement ID (Admin → Data Streams → Web Stream)
    // 형식: 'G-9QC121BKET'
    GA4_MEASUREMENT_ID: 'G-9QC121BKET',

    // Zapier Catch Webhook URL (선택 · Slack 알림 / Sheet 백업)
    // 형식: 'https://hooks.zapier.com/hooks/catch/...'
    ZAPIER_WEBHOOK: 'https://script.google.com/macros/s/AKfycbykOqNs2eT7Y72a8MKdi5eIRViC6l5K11cQBgnf5Kal8QACmz9HjFTcr73LnVyWq-E/exec',

    // 언어별 커뮤니티 URL · 사전등록 후 안내에 사용
    // ko / en / ja (all Discord)
    COMMUNITY_URLS: {
      ko: 'https://discord.gg/GgSBUzHTZ',  // Discord
      en: 'https://discord.gg/GgSBUzHTZ',  // Discord
      ja: 'https://discord.gg/GgSBUzHTZ',  // Discord
    },

    /* ─────────────── 옵션 ─────────────── */

    // 디버그 모드: API 미호출, 콘솔 로그만
    DEBUG: false,
  };

  const KLAVIYO_API = 'https://a.klaviyo.com/client';
  const KLAVIYO_REVISION = '2024-10-15';

  function isOk(key){ return !!CONFIG[key] && CONFIG[key].length > 0; }
  function dbg(...args){ if(CONFIG.DEBUG) console.log('[LUCIVE]', ...args); }

  /**
   * 현재 페이지의 언어 감지 (ISO 639-1 2자리 코드).
   * 우선순위: <html lang> → URL ?lang= → navigator.language → 'ko' fallback
   */
  function detectLang(){
    const supported = ['ko','en','ja'];
    const fromHtml = (document.documentElement.lang || '').toLowerCase().split('-')[0];
    if(supported.includes(fromHtml)) return fromHtml;
    const fromUrl = new URLSearchParams(location.search).get('lang');
    if(fromUrl && supported.includes(fromUrl.toLowerCase())) return fromUrl.toLowerCase();
    const fromNav = (navigator.language || 'ko').toLowerCase().split('-')[0];
    if(supported.includes(fromNav)) return fromNav;
    return 'ko';
  }

  /** 언어별 커뮤니티 URL 반환 */
  function communityUrl(lang){
    lang = lang || detectLang();
    return (CONFIG.COMMUNITY_URLS && CONFIG.COMMUNITY_URLS[lang]) || CONFIG.COMMUNITY_URLS.ko || '';
  }

  /** properties 에 language 자동 주입 */
  function withLang(props){
    props = props || {};
    if(!props.language) props.language = detectLang();
    return props;
  }

  /* ─────────────── Klaviyo ─────────────── */

  /**
   * 이메일을 Klaviyo 리스트에 구독시킨다 (마케팅 동의).
   * 동시에 프로필 properties 도 저장.
   * @returns {Promise<boolean>}
   */
  async function klaviyoSubscribe(email, properties){
    properties = withLang(properties);
    if(!isOk('KLAVIYO_PUBLIC_KEY') || !isOk('KLAVIYO_LIST_ID')){
      dbg('subscribe skipped (no key/list)', email, properties);
      return false;
    }
    if(CONFIG.DEBUG){ dbg('subscribe (debug)', email, properties); return true; }
    try{
      const res = await fetch(KLAVIYO_API + '/subscriptions/?company_id=' + CONFIG.KLAVIYO_PUBLIC_KEY, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'revision': KLAVIYO_REVISION },
        body: JSON.stringify({
          data: {
            type: 'subscription',
            attributes: {
              profile: { data: { type: 'profile', attributes: { email: email, properties: properties } } },
              custom_source: 'pre-register-form'
            },
            relationships: { list: { data: { type: 'list', id: CONFIG.KLAVIYO_LIST_ID } } }
          }
        })
      });
      dbg('subscribe', email, res.status);
      return res.ok || res.status === 202;
    }catch(e){ console.error('Klaviyo subscribe failed', e); return false; }
  }

  /**
   * 기존 프로필의 properties 를 업데이트 (구독 X, 속성만 갱신).
   * 설문 응답 같은 추가 데이터를 저장할 때 사용.
   */
  async function klaviyoIdentify(email, properties){
    properties = withLang(properties);
    if(!isOk('KLAVIYO_PUBLIC_KEY')){
      dbg('identify skipped (no key)', email, properties);
      return false;
    }
    if(CONFIG.DEBUG){ dbg('identify (debug)', email, properties); return true; }
    try{
      const res = await fetch(KLAVIYO_API + '/profiles/?company_id=' + CONFIG.KLAVIYO_PUBLIC_KEY, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'revision': KLAVIYO_REVISION },
        body: JSON.stringify({
          data: { type: 'profile', attributes: { email: email, properties: properties } }
        })
      });
      dbg('identify', email, res.status);
      return res.ok || res.status === 202;
    }catch(e){ console.error('Klaviyo identify failed', e); return false; }
  }

  /**
   * 커스텀 이벤트 발사 (Klaviyo Flow 트리거 가능).
   * 예: 'Pre-registered', 'Survey Completed', 'Share Clicked'
   */
  async function klaviyoTrack(email, eventName, properties){
    properties = properties || {};
    if(!isOk('KLAVIYO_PUBLIC_KEY')){
      dbg('track skipped (no key)', email, eventName, properties);
      return false;
    }
    if(CONFIG.DEBUG){ dbg('track (debug)', email, eventName, properties); return true; }
    try{
      const res = await fetch(KLAVIYO_API + '/events/?company_id=' + CONFIG.KLAVIYO_PUBLIC_KEY, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'revision': KLAVIYO_REVISION },
        body: JSON.stringify({
          data: {
            type: 'event',
            attributes: {
              properties: properties,
              metric: { data: { type: 'metric', attributes: { name: eventName } } },
              profile: { data: { type: 'profile', attributes: { email: email } } }
            }
          }
        })
      });
      dbg('track', email, eventName, res.status);
      return res.ok || res.status === 202;
    }catch(e){ console.error('Klaviyo track failed', e); return false; }
  }

  /* ─────────────── GA4 ─────────────── */

  // 페이지 로드 시 자동 초기화 (CONFIG 에 ID 있으면 gtag.js 동적 삽입)
  function initGA4(){
    if(!isOk('GA4_MEASUREMENT_ID')) return;
    const id = CONFIG.GA4_MEASUREMENT_ID;
    if(window.gtag) return; // 이미 초기화됨
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, { send_page_view: true });
    dbg('GA4 initialized', id);
  }

  /**
   * GA4 이벤트 발사. gtag 미로드 시 무동작.
   * 표준 이벤트: sign_up, share, select_content, ...
   * 커스텀: survey_complete, cta_click, demo_started, ...
   */
  function gaEvent(eventName, params){
    params = params || {};
    if(typeof window.gtag === 'function'){
      window.gtag('event', eventName, params);
      dbg('GA4 event', eventName, params);
    }else{
      dbg('GA4 not loaded, skipped', eventName, params);
    }
  }

  /* ─────────────── Zapier (선택) ─────────────── */

  /**
   * Zapier Catch Webhook 으로 페이로드 전송.
   * Slack 알림 / Google Sheet 백업 / 그 외 자동화에 사용.
   */
  async function zapierWebhook(payload){
    if(!isOk('ZAPIER_WEBHOOK')){
      dbg('zapier skipped (no webhook)', payload);
      return false;
    }
    if(CONFIG.DEBUG){ dbg('zapier (debug)', payload); return true; }
    try{
      // no-cors: Google Apps Script는 OPTIONS preflight를 처리하지 않으므로
      // Content-Type 헤더 없이 보내야 preflight가 생략되어 실제 POST가 도달한다.
      // Apps Script에서는 e.postData.contents 를 JSON.parse 해서 읽으면 된다.
      const enriched = Object.assign({ language: detectLang() }, payload);
      await fetch(CONFIG.ZAPIER_WEBHOOK, {
        method: 'POST',
        mode: 'no-cors',
        body: JSON.stringify(enriched)
      });
      dbg('zapier sent (no-cors)');
      return true;
    }catch(e){ console.error('Zapier webhook failed', e); return false; }
  }

  /* ─────────────── 초기화 ─────────────── */

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initGA4);
  }else{
    initGA4();
  }

  /* ─────────────── public API ─────────────── */

  return {
    CONFIG: CONFIG,
    klaviyoSubscribe: klaviyoSubscribe,
    klaviyoIdentify: klaviyoIdentify,
    klaviyoTrack: klaviyoTrack,
    gaEvent: gaEvent,
    zapierWebhook: zapierWebhook,
    detectLang: detectLang,
    communityUrl: communityUrl,
  };
})();
