let chapters = [];
let loadedChapters = {};
let activeQuestions = [];
let current = 0;
let correct = 0;

const menu = document.getElementById("menu");
const chapterSelect = document.getElementById("chapterSelect");
const quiz = document.getElementById("quiz");
const result = document.getElementById("result");

// ======= INIT ========
fetch("data/meta.json")
.then(r => r.json())
.then(data => {
    chapters = data.chapters;
});

// ======= UI ========
function openChapterMode(){
    menu.classList.add("hidden");
    chapterSelect.classList.remove("hidden");

    chapterSelect.innerHTML = `<h2>Kapitel wählen</h2>`;

    chapters.forEach(ch => {
        let btn = document.createElement("button");
        btn.innerText = ch;
        btn.onclick = () => loadChapter(ch);
        chapterSelect.appendChild(btn);
    });
}

function loadChapter(name){
    if(loadedChapters[name]){
        startQuiz(loadedChapters[name].questions);
        return;
    }

    fetch(`data/${name}.json`)
    .then(r => r.json())
    .then(data => {
        loadedChapters[name] = data;
        startQuiz(data.questions);
    });
}

// ======= EXAM MODE ========
async function startExam(){
    let allQuestions = [];

    for(const c of chapters){
        if(!loadedChapters[c]){
            const r = await fetch(`data/${c}.json`);
            loadedChapters[c] = await r.json();
        }
        allQuestions.push(...loadedChapters[c].questions);
    }

    startQuiz(shuffle(allQuestions).slice(0,30));
}

// ======= QUIZ ========
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
    if(current >= activeQuestions.length){
        return showResult();
    }

    const q = activeQuestions[current];
    quiz.innerHTML = `
        <h2>Frage ${current+1} / ${activeQuestions.length}</h2>
        <div class="question">${q.question}</div>
    `;

    if(q.image){
        const img = document.createElement("img");
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

    setTimeout(()=>{
        current++;
        loadQuestion();
    },700);
}

function showResult(){
    quiz.classList.add("hidden");
    result.classList.remove("hidden");

    result.innerHTML = `
        <h2>Ergebnis</h2>
        <p>${correct} von ${activeQuestions.length} richtig</p>
        <button onclick="location.reload()">Zurück zum Start</button>
    `;
}

function shuffle(arr){
    return arr.sort(()=>Math.random()-0.5);
}
