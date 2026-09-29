const posterFiles = [
  "115地方基層公職人員選舉反賄選宣導電子_1.jpg",
  "115地方基層公職人員選舉反賄選宣導電子_2.jpg",
  "115地方基層公職人員選舉反賄選宣導電子_3.jpg",
  "115地方基層公職人員選舉反賄選宣導電子_4.jpg",
  "115地方基層公職人員選舉反賄選宣導電子_5.jpg",
  "241211_法務部_反詐騙_1.jpg",
  "241211_法務部_反詐騙_3.jpg",
  "241211_法務部_反詐騙_4.jpg",
  "241211_法務部_反詐騙_5.jpg",
  "241213_法務部_反詐騙_2.jpg",
  "廉政倫理登入.png",
  "揭弊宣導海報1.jpg",
  "揭弊宣導海報2.jpg",
  "法務部_反賄選海報_a_a1.jpg",
  "法務部_反賄選海報_b_a1.jpg",
  "誠風破浪的臺北隊宣導圖卡22款_1.png",
  "誠風破浪的臺北隊宣導圖卡22款_2.png",
  "誠風破浪的臺北隊宣導圖卡22款_3.png",
  "誠風破浪的臺北隊宣導圖卡22款_4.png",
  "誠風破浪的臺北隊宣導圖卡22款_5.png",
  "透明金質獎.jpg"
];
const blessings = [
  "祝你今天順心如意",
  "願你的每一步都走向好事",
  "今天也會有值得開心的小事發生",
  "願你被溫柔對待，也記得善待自己",
  "好運正在路上，請保持期待",
  "願今天的你平安、自在、充滿力量",
  "小小的努力，正在累積成大大的幸運",
  "願你的笑容比陽光更早抵達"
];

const stage = document.querySelector(".machine-stage");
const capsule = document.querySelector("#capsule-result");
const drawButton = document.querySelector("#draw-button");
const statusMessage = document.querySelector("#status-message");
const modal = document.querySelector("#modal");
let lastIndex = -1;
let currentReminder = null;
const posterCache = new Map();

function preloadPoster(filename) {
  if (!posterCache.has(filename)) {
    const image = new Image();
    const loaded = new Promise((resolve, reject) => {
      image.onload = () => resolve(image);
      image.onerror = reject;
    });
    image.src = `宣導用/${encodeURIComponent(filename)}`;
    posterCache.set(filename, loaded);
  }
  return posterCache.get(filename);
}

function draw() {
  if (stage.classList.contains("is-spinning")) return;
  let index;
  do { index = Math.floor(Math.random() * posterFiles.length); } while (posterFiles.length > 1 && index === lastIndex);
  currentReminder = posterFiles[index];
  lastIndex = index;
  stage.classList.remove("has-result");
  stage.classList.add("is-spinning");
  drawButton.disabled = true;
  statusMessage.textContent = "扭蛋機轉動中，今天的提醒正在靠近……";
  Promise.all([preloadPoster(currentReminder), new Promise(resolve => setTimeout(resolve, 1050))]).then(() => {
    stage.classList.remove("is-spinning");
    stage.classList.add("has-result");
    statusMessage.textContent = "扭蛋掉出來了，點一下把提醒打開！";
    drawButton.disabled = false;
    drawButton.innerHTML = "<span>✦</span> 再抽一顆";
  }).catch(() => {
    stage.classList.remove("is-spinning");
    drawButton.disabled = false;
    statusMessage.textContent = "圖片載入失敗，請再試一次。";
  });
}

function openCapsule() {
  if (!currentReminder || stage.classList.contains("is-spinning")) return;
  const posterImage = document.querySelector("#poster-image");
  preloadPoster(currentReminder).then(() => {
    posterImage.src = `宣導用/${encodeURIComponent(currentReminder)}`;
    posterImage.alt = `抽到的宣導圖片：${currentReminder}`;
  });
  document.querySelector("#result-category").textContent = "今日運勢";
  document.querySelector("#result-title").textContent = blessings[Math.floor(Math.random() * blessings.length)];
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal() { modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); }
drawButton.addEventListener("click", draw);
capsule.addEventListener("click", openCapsule);
capsule.addEventListener("keydown", event => { if (event.key === "Enter" || event.key === " ") openCapsule(); });
document.querySelector("#close-modal").addEventListener("click", closeModal);
document.querySelector("#again-button").addEventListener("click", () => { closeModal(); draw(); });
modal.addEventListener("click", event => { if (event.target === modal) closeModal(); });
document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
