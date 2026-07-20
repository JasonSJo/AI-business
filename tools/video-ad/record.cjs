// 15초 세로형 광고를 녹화해 webm으로 저장한다.
// 사용: node record.cjs  (저장소 루트에서 http.server 로 서빙 중이어야 함)
const { chromium } = require('/opt/node22/lib/node_modules/playwright/index.js');

(async () => {
  const OUT = __dirname + '/out';
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({
    viewport: { width: 1080, height: 1920 },
    recordVideo: { dir: OUT, size: { width: 1080, height: 1920 } },
  });
  const p = await ctx.newPage();
  await p.goto('http://localhost:8896/tools/video-ad/ad-15s.html', { waitUntil: 'networkidle', timeout: 30000 });
  await p.evaluate(() => Promise.all([document.fonts.ready,
    ...[...document.images].map(i => i.complete ? 0 : new Promise(r => i.onload = i.onerror = r))]));
  await p.waitForTimeout(400);
  await p.evaluate(() => document.body.classList.add('play')); // 타임라인 시작
  await p.waitForTimeout(15600);
  const video = p.video();
  await ctx.close();
  const path = await video.path();
  await b.close();
  console.log('WEBM=' + path);
})();
