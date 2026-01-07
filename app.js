let chapters = [];
let loadedChapters = {};
let activeQuestions = [];
let current = 0;
let correct = 0;
let userAnswers = []; // Track user's answers for each question

const chapterSelect = document.getElementById("chapterSelect");
const chapterReview = document.getElementById("chapterReview");
const quiz = document.getElementById("quiz");
const result = document.getElementById("result");

// ======= HELPER FUNCTIONS ========
function formatChapterDisplayName(filename) {
    return filename.replace('.json', '').replace(/-/g, ' ');
}

// ======= INIT ========
fetch("data/meta.json")
.then(r => r.json())
.then(data => {
    chapters = data.chapters;
});

// ======= UI ========
async function openChapterMode(){
    chapterSelect.classList.remove("hidden");
    chapterReview.classList.add("hidden");
    quiz.classList.add("hidden");
    result.classList.add("hidden");

    chapterSelect.innerHTML = `
        <h2>Kapitel wählen</h2>
    `;

    for(const ch of chapters){
        if(!loadedChapters[ch]){
            const r = await fetch(`data/${ch}`);
            loadedChapters[ch] = await r.json();
        }
        
        const questionCount = loadedChapters[ch].questions.length;
        let btn = document.createElement("button");
        btn.innerText = `${formatChapterDisplayName(ch)} (${questionCount})`;
        btn.onclick = () => loadChapter(ch);
        chapterSelect.appendChild(btn);
    }
}

function loadChapter(name){
    if(loadedChapters[name]){
        startQuiz(loadedChapters[name].questions);
        return;
    }

    fetch(`data/${name}`)
    .then(r => r.json())
    .then(data => {
        loadedChapters[name] = data;
        startQuiz(data.questions);
    });
}

// ======= CHAPTER REVIEW ========
async function openChapterReview(){
    chapterReview.classList.remove("hidden");
    chapterSelect.classList.add("hidden");
    quiz.classList.add("hidden");
    result.classList.add("hidden");

    chapterReview.innerHTML = `
        <h2>Kapitel nachlesen</h2>
        <div id="reviewChapterList"></div>
    `;

    const listContainer = document.getElementById("reviewChapterList");
    
    for(const ch of chapters){
        if(!loadedChapters[ch]){
            const r = await fetch(`data/${ch}`);
            loadedChapters[ch] = await r.json();
        }
        
        const questionCount = loadedChapters[ch].questions.length;
        let btn = document.createElement("button");
        btn.innerText = `${formatChapterDisplayName(ch)} (${questionCount})`;
        btn.className = "chapter-btn";
        btn.onclick = () => showChapterContent(ch);
        listContainer.appendChild(btn);
    }
}

async function showChapterContent(name){
    if(!loadedChapters[name]){
        const r = await fetch(`data/${name}`);
        loadedChapters[name] = await r.json();
    }

    const chapter = loadedChapters[name];
    const displayName = formatChapterDisplayName(name);
    
    chapterReview.innerHTML = `
        <h2>${displayName}</h2>
        <button onclick="openChapterReview()" class="back-btn">Zurück zur Übersicht</button>
        <div class="chapter-content"></div>
    `;

    const content = chapterReview.querySelector('.chapter-content');
    
    chapter.questions.forEach((q, index) => {
        const qaItem = document.createElement("div");
        qaItem.className = "qa-item";
        qaItem.innerHTML = `
            <div class="qa-number">${index + 1}.</div>
            <div class="qa-details">
                <div class="qa-question">${q.question}</div>
                ${q.image ? `<img src="${q.image}" class="pictogram" alt="Frage Bild">` : ''}
                <div class="qa-answers">
                    ${q.answers.map((a, i) => `
                        <div class="qa-answer ${i === q.correctIndex ? 'qa-correct' : ''}">
                            ${i === q.correctIndex ? '✓ ' : ''}${a}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        content.appendChild(qaItem);
    });
}

// ======= EXAM MODE ========
async function startExam(){
    let allQuestions = [];

    for(const c of chapters){
        if(!loadedChapters[c]){
            const r = await fetch(`data/${c}`);
            loadedChapters[c] = await r.json();
        }
        allQuestions.push(...loadedChapters[c].questions);
    }

    startQuiz(shuffle(allQuestions).slice(0,30));
}

// ======= QUIZ ========
function startQuiz(list){
    chapterSelect.classList.add("hidden");
    chapterReview.classList.add("hidden");
    result.classList.add("hidden");
    quiz.classList.remove("hidden");

    activeQuestions = shuffle(list);
    current = 0;
    correct = 0;
    userAnswers = []; // Reset user answers for new quiz
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

    // Store user's answer
    userAnswers.push({
        question: q,
        userAnswerIndex: i,
        isCorrect: i === q.correctIndex
    });

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
    chapterSelect.classList.add("hidden");
    chapterReview.classList.add("hidden");
    result.classList.remove("hidden");

    const totalQuestions = activeQuestions.length;
    const percentage = Math.round((correct / totalQuestions) * 100);
    
    // Filter incorrect answers
    const incorrectAnswers = userAnswers.filter(ua => !ua.isCorrect);

    let resultHTML = `
        <h2>Ergebnis</h2>
        <p>${correct} von ${totalQuestions} richtig (${percentage}%)</p>
    `;

    // Show incorrect questions if any
    if(incorrectAnswers.length > 0){
        resultHTML += `
            <div class="incorrect-section">
                <h3>Falsch beantwortete Fragen:</h3>
                <div class="incorrect-questions">
        `;

        incorrectAnswers.forEach((ua, index) => {
            const q = ua.question;
            resultHTML += `
                <div class="incorrect-item">
                    <div class="incorrect-number">${index + 1}.</div>
                    <div class="incorrect-details">
                        <div class="incorrect-question">${q.question}</div>
                        ${q.image ? `<img src="${q.image}" class="pictogram" alt="Frage Bild">` : ''}
                        <div class="incorrect-answers">
                            ${q.answers.map((a, i) => {
                                let classes = 'incorrect-answer';
                                let prefix = '';
                                
                                if(i === q.correctIndex){
                                    classes += ' answer-correct-review';
                                    prefix = '✓ ';
                                }
                                if(i === ua.userAnswerIndex){
                                    classes += ' answer-wrong-review';
                                    prefix = '✗ ';
                                }
                                
                                return `<div class="${classes}">${prefix}${a}</div>`;
                            }).join('')}
                        </div>
                    </div>
                </div>
            `;
        });

        resultHTML += `
                </div>
            </div>
        `;
    }

    result.innerHTML = resultHTML;
}

function shuffle(arr){
    return arr.sort(()=>Math.random()-0.5);
}
