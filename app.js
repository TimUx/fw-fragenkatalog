let questions = [];
let current = 0;
let correct = 0;
let activeQuestions = [];

const menu = document.getElementById("menu");
const chapterSelect = document.getElementById("chapterSelect");
const quiz = document.getElementById("quiz");
const result = document.getElementById("result");

fetch("data/questions.json")
.then(r => r.json())
.then(data => { questions = data; });

function openChapterMode(){
    menu.classList.add("hidden");
    chapterSelect.classList.remove("hidden");
    chapterSelect.innerHTML = `<h2>Kapitel wählen</h2>`;
    Object.keys(questions).forEach(k => {
        let btn = document.createElement("button");
        btn.innerText = k;
        btn.onclick = () => startQuiz(questions[k]);
        chapterSelect.appendChild(btn);
    });
}
function startExam(){
    let all = [];
    Object.values(questions).forEach(q => all.push(...q));
    startQuiz(shuffle(all).slice(0,30));
}
function startQuiz(list){
    chapterSelect.classList.add("hidden");
    result.classList.add("hidden");
    quiz.classList.remove("hidden");
    activeQuestions = shuffle(list);
    current = 0;
    correct = 0;
    loadQuestion();
}
function loadQuestion(){
    if(current >= activeQuestions.length) return showResult();
    const q = activeQuestions[current];
    quiz.innerHTML = `<h2>Frage ${current+1} / ${activeQuestions.length}</h2>
        <div class='question'>${q.question}</div>`;
    if(q.image){
        let img = document.createElement("img");
        img.src = q.image;
        img.className = "pictogram";
        quiz.appendChild(img);
    }
    q.answers.forEach((a,i)=>{
        let div = document.createElement("div");
        div.className = "answer";
        div.innerText = a;
        div.onclick = ()=>answer(i);
        quiz.appendChild(div);
    });
}
function answer(i){
    const q = activeQuestions[current];
    const answers = document.querySelectorAll(".answer");
    if(i === q.correctIndex){
        answers[i].classList.add("correct");
        correct++;
    } else {
        answers[i].classList.add("wrong");
        answers[q.correctIndex].classList.add("correct");
    }
    setTimeout(()=>{ current++; loadQuestion(); },800);
}
function showResult(){
    quiz.classList.add("hidden");
    result.classList.remove("hidden");
    result.innerHTML = `<h2>Ergebnis</h2>
        <p>${correct} von ${activeQuestions.length} richtig</p>
        <button onclick='location.reload()'>Zurück zum Start</button>`;
}
function shuffle(arr){ return arr.sort(()=>Math.random()-0.5); }
