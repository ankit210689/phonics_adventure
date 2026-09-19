const letters = [
  ["A", "a", "short a", "ah", "APPLE", "🍎", ["APPLE", "BALL", "CAT"]], ["B", "b", "b", "buh", "BALL", "⚽", ["DOG", "BALL", "SUN"]], ["C", "c", "k", "kuh", "CAT", "🐱", ["CAT", "DOG", "FISH"]], ["D", "d", "d", "duh", "DOG", "🐶", ["SUN", "DOG", "MAP"]], ["E", "e", "short e", "eh", "EGG", "🥚", ["EGG", "FISH", "BALL"]], ["F", "f", "f", "fff", "FISH", "🐟", ["CAT", "FISH", "DOG"]], ["G", "g", "g", "guh", "GOAT", "🐐", ["GOAT", "SUN", "APPLE"]], ["H", "h", "h", "huh", "HAT", "🎩", ["HAT", "DOG", "FISH"]], ["I", "i", "short i", "ih", "IGLOO", "🏠", ["BALL", "IGLOO", "CAT"]], ["J", "j", "j", "juh", "JAM", "🍓", ["JAM", "DOG", "SUN"]], ["K", "k", "k", "kuh", "KITE", "🪁", ["KITE", "APPLE", "FISH"]], ["L", "l", "l", "lll", "LION", "🦁", ["DOG", "LION", "BALL"]], ["M", "m", "m", "mmm", "MOON", "🌙", ["MOON", "CAT", "SUN"]], ["N", "n", "n", "nnn", "NOSE", "👃", ["FISH", "NOSE", "BALL"]], ["O", "o", "short o", "ah", "OCTOPUS", "🐙", ["DOG", "OCTOPUS", "HAT"]], ["P", "p", "p", "puh", "PIG", "🐷", ["PIG", "SUN", "CAT"]], ["Q", "q", "qu", "kwuh", "QUEEN", "👑", ["BALL", "QUEEN", "DOG"]], ["R", "r", "r", "rrr", "RABBIT", "🐰", ["RABBIT", "FISH", "APPLE"]], ["S", "s", "s", "sss", "SUN", "☀️", ["SUN", "DOG", "BALL"]], ["T", "t", "t", "tuh", "TIGER", "🐯", ["CAT", "TIGER", "FISH"]], ["U", "u", "short u", "uh", "UMBRELLA", "☂️", ["UMBRELLA", "DOG", "BALL"]], ["V", "v", "v", "vvv", "VAN", "🚐", ["SUN", "VAN", "CAT"]], ["W", "w", "w", "wuh", "WATER", "💧", ["WATER", "DOG", "APPLE"]], ["X", "x", "x", "ks", "XRAY", "🩻", ["XRAY", "SUN", "DOG"]], ["Y", "y", "y", "yuh", "YO-YO", "🪀", ["CAT", "YO-YO", "BALL"]], ["Z", "z", "z", "zuh", "ZEBRA", "🦓", ["ZEBRA", "DOG", "FISH"]]
].map(([uppercase, lowercase, phonics, sound, word, emoji, choices]) => ({ uppercase, lowercase, phonics, sound, word, emoji, choices }));

let currentIndex = 0;
let stars = 0;
let quizIndex = 0;
let answered = false;
const $ = (id) => document.getElementById(id);

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.38;
  utterance.pitch = 0.9;
  utterance.volume = 1;
  window.speechSynthesis.speak(utterance);
}

function renderLesson() {
  const letter = letters[currentIndex];
  $("uppercase-letter").textContent = letter.uppercase;
  $("lowercase-letter").textContent = letter.lowercase;
  $("letter-emoji").textContent = letter.emoji;
  $("word-label").textContent = `${letter.uppercase} is for`;
  $("word-name").textContent = letter.word;
  $("phonics-sound").textContent = letter.phonics;
  $("letter-number").textContent = String(currentIndex + 1).padStart(2, "0");
  $("progress-label").textContent = `${currentIndex + 1} / ${letters.length}`;
  $("progress-bar").style.width = `${((currentIndex + 1) / letters.length) * 100}%`;
  $("previous-letter").disabled = currentIndex === 0;
}

function renderQuiz() {
  const letter = letters[quizIndex];
  $("quiz-progress").textContent = `Question ${quizIndex + 1} of ${letters.length}`;
  $("quiz-letter").textContent = letter.uppercase;
  $("quiz-phonetic").textContent = `/${letter.phonics}/`;
  $("choice-list").innerHTML = "";
  $("quiz-feedback").textContent = "";
  $("next-question").classList.add("hidden");
  answered = false;
  letter.choices.forEach((choice) => {
    const button = document.createElement("button");
    button.className = "choice-button";
    button.textContent = choice;
    button.addEventListener("click", () => answerQuiz(button, choice, letter));
    $("choice-list").append(button);
  });
}

function answerQuiz(button, choice, letter) {
  if (answered) return;
  answered = true;
  const correct = choice === letter.word;
  button.classList.add(correct ? "correct" : "wrong");
  if (correct) { stars += 1; $("star-count").textContent = stars; $("quiz-feedback").textContent = "Brilliant! You found it. +1 star"; speak(`${letter.word}. Great job!`); }
  else { $("quiz-feedback").textContent = `Almost! The answer is ${letter.word}.`; [...$("choice-list").children].find((item) => item.textContent === letter.word).classList.add("correct"); speak(letter.word); }
  $("next-question").classList.remove("hidden");
}

document.querySelectorAll(".mode-tab").forEach((tab) => tab.addEventListener("click", () => {
  document.querySelectorAll(".mode-tab").forEach((item) => item.classList.toggle("active", item === tab));
  $("learn-panel").classList.toggle("hidden", tab.dataset.mode !== "learn");
  $("quiz-panel").classList.toggle("hidden", tab.dataset.mode !== "quiz");
  if (tab.dataset.mode === "quiz") renderQuiz();
}));
$("previous-letter").addEventListener("click", () => { if (currentIndex > 0) { currentIndex -= 1; renderLesson(); } });
$("next-letter").addEventListener("click", () => { currentIndex = (currentIndex + 1) % letters.length; renderLesson(); });
$("say-letter").addEventListener("click", () => { const l = letters[currentIndex]; speak(`Letter ${l.uppercase}. Capital ${l.uppercase}. Small ${l.lowercase}. The sound is ${l.sound}. ${l.uppercase} is for ${l.word}.`); });
$("say-sound").addEventListener("click", () => {
  const l = letters[currentIndex];
  const soundText = l.uppercase === "A"
    ? "A... pause... sounds like... Aaeh"
    : `${l.uppercase}... pause... sounds like... ${l.sound}`;
  speak(soundText);
});
$("say-word").addEventListener("click", () => speak(letters[currentIndex].word));
$("next-question").addEventListener("click", () => { quizIndex = (quizIndex + 1) % letters.length; renderQuiz(); });
renderLesson();