class FlagGame {
  constructor() {
    this.encryptedFlag = "CB0IUxsUCFhWEl9RBUAZWBM=";
    this.secretKey = "a2luZ3lvZmxhZzIwMjU=";
    this.flag = this.decryptFlag();
    this.tank = document.getElementById("tank");
    this.flagContainer = document.getElementById("flag-container");
    this.collectedFlag = document.getElementById("collected-flag");
    this.resultOverlay = document.getElementById("result-overlay");
    this.resultText = document.getElementById("result-text");
    this.restartBtn = document.getElementById("restart-btn");
    this.characters = [];
    this.animationId = null;
    this.tankWidth = 0;
    this.tankHeight = 0;
    this.init();
  }
  init() {
    this.setupTankDimensions();
    this.createFlagCharacters();
    this.startAnimation();
    this.setupEventListeners();
    window.addEventListener("resize", () => this.handleResize());
  }
  setupEventListeners() {
    this.restartBtn.addEventListener("click", () => this.restartGame());
  }
  decryptFlag() {
    try {
      const key = atob(this.secretKey);
      const encryptedBytes = atob(this.encryptedFlag);
      let decrypted = "";
      for (let i = 0; i < encryptedBytes.length; i++) {
        const keyChar = key.charCodeAt(i % key.length);
        const encryptedChar = encryptedBytes.charCodeAt(i);
        decrypted += String.fromCharCode(encryptedChar ^ keyChar);
      }
      return decrypted;
    } catch (error) {
      return "decrypt error";
    }
  }
  shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }
  setupTankDimensions() {
    const rect = this.tank.getBoundingClientRect();
    this.tankWidth = rect.width - 10;
    this.tankHeight = rect.height - 10;
  }
  createFlagCharacters() {
    this.flagContainer.innerHTML = "";
    this.characters = [];
    const indices = Array.from({ length: this.flag.length }, (_, i) => i);
    this.shuffleArray(indices);
    for (let j = 0; j < indices.length; j++) {
      const i = indices[j];
      const char = this.flag[i];
      const charElement = document.createElement("div");
      charElement.className = "flag-char";
      charElement.textContent = char;
      charElement.dataset.index = i;
      const character = {
        element: charElement,
        x: Math.random() * (this.tankWidth - 40),
        y: Math.random() * (this.tankHeight - 40),
        vx: (Math.random() - 0.5) * 3,
        vy: (Math.random() - 0.5) * 3,
        collected: false,
        index: i,
      };
      charElement.style.left = character.x + "px";
      charElement.style.top = character.y + "px";
      charElement.addEventListener("click", (e) =>
        this.collectCharacter(character, e)
      );
      this.flagContainer.appendChild(charElement);
      this.characters.push(character);
    }
  }
  collectCharacter(character, event) {
    if (character.collected) return;
    character.collected = true;
    character.element.classList.add("collected");
    const currentFlag = this.collectedFlag.textContent;
    this.collectedFlag.textContent =
      currentFlag + character.element.textContent;
    setTimeout(() => {
      if (character.element.parentNode) {
        character.element.parentNode.removeChild(character.element);
      }
    }, 200);
    this.checkGameComplete();
    event.stopPropagation();
  }
  checkGameComplete() {
    const allCollected = this.characters.every((char) => char.collected);
    if (allCollected) {
      setTimeout(() => {
        this.showResult();
      }, 500);
    }
  }
  showResult() {
    const collectedFlag = this.collectedFlag.textContent;
    const isCorrect = collectedFlag === this.flag;
    this.resultText.textContent = isCorrect ? "🎉 Correct! 🎉" : "❌ Incorrect ❌";
    this.resultText.className = `result-text ${
      isCorrect ? "correct" : "incorrect"
    }`;
    this.resultOverlay.classList.add("show");
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
  }
  restartGame() {
    this.resultOverlay.classList.remove("show");
    this.collectedFlag.textContent = "";
    this.createFlagCharacters();
    this.startAnimation();
  }
  updateCharacterPositions() {
    this.characters.forEach((character) => {
      if (character.collected) return;
      character.x += character.vx;
      character.y += character.vy;
      if (character.x <= 0 || character.x >= this.tankWidth - 30) {
        character.vx = -character.vx;
        character.x = Math.max(0, Math.min(this.tankWidth - 30, character.x));
      }
      if (character.y <= 0 || character.y >= this.tankHeight - 30) {
        character.vy = -character.vy;
        character.y = Math.max(0, Math.min(this.tankHeight - 30, character.y));
      }
      character.element.style.left = character.x + "px";
      character.element.style.top = character.y + "px";
    });
  }
  startAnimation() {
    const animate = () => {
      this.updateCharacterPositions();
      this.animationId = requestAnimationFrame(animate);
    };
    animate();
  }
  handleResize() {
    this.setupTankDimensions();
    this.characters.forEach((character) => {
      if (!character.collected) {
        character.x = Math.min(character.x, this.tankWidth - 30);
        character.y = Math.min(character.y, this.tankHeight - 30);
      }
    });
  }
  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    window.removeEventListener("resize", this.handleResize);
  }
}
document.addEventListener("DOMContentLoaded", () => {
  new FlagGame();
});
