// select all elements
const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const question = document.getElementById("question");
const choiceA = document.getElementById("A");
const choiceB = document.getElementById("B");
const choiceC = document.getElementById("C");
const choiceD = document.getElementById("D");
const counter = document.getElementById("counter");
const timeGauge = document.getElementById("timeGauge");
const progress = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");

// create our questions
let questions = [
    {
        question : "What is the benefit of planting trees around your house?",
        choiceA : "A)&nbsp;Get more oxygen ",
        choiceB : "B)&nbsp;Get more dust ",
        choiceC : "C)&nbsp;Get more pollution ",
        choiceD : "D)&nbsp;Get more ants",
        correct : "A"
    },{
        question : "Why should the use of toxic chemicals be avoided?",
        choiceA : "A)&nbsp;They are not good for human health",
        choiceB : "B)&nbsp;They are harmful to plants and animals",
        choiceC : "C)&nbsp;They pollute natural resources",
        choiceD : "D)&nbsp;All answers are correct",
        correct : "D"
    },{
        question : "How can you reduce energy usage?",
        choiceA : "A)&nbsp;Staying inside when it is cold",
        choiceB : "B)&nbsp;Turning off lights when not in use",
        choiceC : "C)&nbsp;Using older appliances",
        choiceD : "D)&nbsp;Staying outside when it is hot",
        correct : "B"
      },{
        question : "Which of the following gases does not play a part in the greenhouse effect?",
        choiceA : "A)&nbsp;Carbon dioxide",
        choiceB : "B)&nbsp;Water vapor",
        choiceC : "C)&nbsp;Methane",
        choiceD : "D)&nbsp;Nitrogen",
        correct : "D"
      },{
        question : "So far, most of the strongest impacts of climate change have been observed in:",
        choiceA : "A)&nbsp;All latitudes equally",
        choiceB : "B)&nbsp;Northern latitudes",
        choiceC : "C)&nbsp;The tropics",
        choiceD : "D)&nbsp;Southern latitudes",
        correct : "B"
      },{
        question:  "The average American contributes approximately how much CO2 to the atmosphere per year?",
        choiceA : "A)&nbsp;10 tons",
        choiceB : "B)&nbsp;50 tons",
        choiceC : "C)&nbsp;20 tons",
        choiceD : "D)&nbsp;2 tons",
        correct : "C"
      },{
        question:  "The likelihood of which extreme weather event is expected to increase with climate change?",
        choiceA : "A)&nbsp;Hurricanes",
        choiceB : "B)&nbsp;Droughts",
        choiceC : "C)&nbsp;Heat waves",
        choiceD : "D)&nbsp;All of these",
        correct : "D"
      },{
        question:  "Which of the following is not a major cause of deforestation?",
        choiceA : "A)&nbsp;Mining",
        choiceB : "B)&nbsp;Hydroelectric development",
        choiceC : "C)&nbsp;Agricultural expansion",
        choiceD : "D)&nbsp;Logging",
        correct : "B"
      },{
        question:  "How much of Earth’s surface is covered by ocean?",
        choiceA : "A)&nbsp;71%",
        choiceB : "B)&nbsp;97%",
        choiceC : "C)&nbsp;50%",
        choiceD : "D)&nbsp;34%",
        correct : "A"
      },{
        question:  "Which of the following are consequences associated with climate change?",
        choiceA : "A)&nbsp;Declining ice sheets",
        choiceB : "B)&nbsp;Increase in surface temperature",
        choiceC : "C)&nbsp;Rising sea levels",
        choiceD : "D)&nbsp;All of these",
        correct : "D"
    }
];

const lastQuestion = questions.length - 1;
let runningQuestion = 0;
let count = 0;
const questionTime = 10; // 5min
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

// render a question
function renderQuestion() {
    let q = questions[runningQuestion];

    question.innerHTML = "<p>"+ q.question +"</p>";
    choiceA.innerHTML = q.choiceA;
    choiceB.innerHTML = q.choiceB;
    choiceC.innerHTML = q.choiceC;
    choiceD.innerHTML = q.choiceD;
	
	choiceA.style.backgroundColor = "white";	
	choiceB.style.backgroundColor = "white";
	choiceC.style.backgroundColor = "white";
	choiceD.style.backgroundColor = "white";
}

start.addEventListener("click",startQuiz);

// start quiz
function startQuiz(){
    start.style.display = "none";
    renderQuestion();
    quiz.style.display = "block";
    renderProgress();
    renderCounter();
    TIMER = setInterval(renderCounter,1000); // 1000ms = 1s // don't change this
}

// render progress
function renderProgress(){
    for(let qIndex = 0; qIndex <= lastQuestion; qIndex++){
        progress.innerHTML += "<div class='prog' id="+ qIndex +"></div>";
    }
}

// counter render
function renderCounter(){
    if(count <= questionTime){
        counter.innerHTML = count;
        timeGauge.style.width = count * gaugeUnit + "px";
        count++
    }else{
        count = 0;
        // change progress color to red
        answerIsWrong();
        if(runningQuestion < lastQuestion){
            runningQuestion++;
            renderQuestion();
        }else{
            // end the quiz and show the score
            clearInterval(TIMER);
            scoreRender();
        }
    }
}

// checkAnswer
function checkAnswer(answer){
    if( answer == questions[runningQuestion].correct){
        // answer is correct
        score++;
        // change progress color to green
        answerIsCorrect();		
		eval('choice'+answer).style.backgroundColor = "#0f0";		
    } else {
        // answer is wrong
        // change progress color to red
        answerIsWrong();
		eval('choice'+answer).style.backgroundColor = "red";
		eval(questions[runningQuestion].correct).style.backgroundColor = "#0f0";
    }
	
    count = 0;
    if(runningQuestion < lastQuestion){
        runningQuestion++;
        //renderQuestion();
		setTimeout(function() {
		  renderQuestion();
		}, 1000);
    }else{
        // end the quiz and show the score
        clearInterval(TIMER);
        scoreRender();
    }
}

// answer is correct
function answerIsCorrect(){
    document.getElementById(runningQuestion).style.backgroundColor = "#0f0";
	//choiceA.style.backgroundColor = "#0f0";
}

// answer is Wrong
function answerIsWrong(){
    document.getElementById(runningQuestion).style.backgroundColor = "#f00";
}

// score render
function scoreRender(){
    scoreDiv.style.display = "block";

    // calculate the amount of question percent answered by the user
    const scorePerCent = Math.round(100 * score/questions.length);

    // choose the image based on the scorePerCent
    let img = (scorePerCent >= 80) ? "static/images/5.png" :
              (scorePerCent >= 60) ? "static/images/4.png" :
              (scorePerCent >= 40) ? "static/images/3.png" :
              (scorePerCent >= 20) ? "static/images/2.png" :
              "static/images/1.png";

    scoreDiv.innerHTML = "<img src="+ img +">";
    
    scoreDiv.innerHTML += "<p>"+ scorePerCent +"%</p>";
    //document.getElementById('myscore').value = scorePerCent;

    if (scorePerCent > 70) {
        document.getElementById("getPoints").disabled = false;
    }
}
