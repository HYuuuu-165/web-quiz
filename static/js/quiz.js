<!-- Haidi Yu 40484424 -->

//Question database
const questionDatabase = [
    {
        question: 'In which year was the \"18-hole\" game created?',
        answer: '1764',
        option: [
            '1648',
            '1874',
            '1764',
            '2022'
        ],
    },
    {
        question: 'Which golf club is normally the longest?',
        answer: 'The 1-wood',
        option: [
            'The 1-wood',
            'The 5-iron',
            'The 9-iron',
            'The Putter'
        ],
    },
    {
        question: 'In golf, par is the predetermined number of strokes that a proficient golfer should require to complete a hole, you now finished a hole two strokes under the par, what term should you use for your score?',
        answer: 'Eagle',
        option: [
            'Birdie',
            'Eagle',
            'Bogey',
            'Albatross'
        ],
    },
    {
        question: 'How many golf clubs can you take with you in a normal match?',
        answer: '14',
        option: [
            '99',
            '6',
            '12',
            '14'
        ],
    },
    {
        question: 'Under what circumstances will a golfer be disqualified?',
        answer: 'None of these',
        option: [
            'A lost ball or a ball hit out of bounds',
            'Making a stroke at the wrong ball',
            'hitting a fellow player\'s ball if both balls lay on the green prior to the stroke',
            'None of these'
        ],
    },
];

const question = document.getElementById('question');
const questionContainer = document.getElementById('container');
const option0 = document.getElementById('option0');
const option1 = document.getElementById('option1');
const option2 = document.getElementById('option2');
const option3 = document.getElementById('option3');
const next = document.querySelector('.next');
const points = document.getElementById('score');
const scoreboard = document.getElementById('scoreboard');
const span = document.querySelectorAll('span');
let i = 0;
let score = 0;

//show questions
function printQuestion(){
    for(let a=0; a<span.length; a++){
        span[a].style.background='none';
    }
    question.innerHTML= 'Question.'+(i+1)+' '+questionDatabase[i].question;
    option0.innerHTML= questionDatabase[i].option[0];
    option1.innerHTML= questionDatabase[i].option[1];
    option2.innerHTML= questionDatabase[i].option[2];
    option3.innerHTML= questionDatabase[i].option[3];
    stage.innerHTML= "Question"+' '+(i+1)+' '+'of'+' '+questionDatabase.length;
}

//add score
function scoring(mark){
    if(mark.innerHTML===questionDatabase[i].answer && score<questionDatabase.length)
    {
        score= score+1;
        document.getElementById(mark.id).style.background= 'green';
    }
    else{
        document.getElementById(mark.id).style.background= 'red';
    }
    setTimeout(nextQuestion,350);
}

//next q
function nextQuestion(){
    if(i<questionDatabase.length-1)
    {
        i=i+1;
        printQuestion();
    }
    else{
        points.innerHTML= score+ '/'+ questionDatabase.length;
        questionContainer.style.display= 'none';
        scoreboard.style.display= 'block'
    }
}
printQuestion();

//when choose next, do
next.addEventListener('click',nextQuestion);

//when choose back to quiz, do
function backToQuiz(){
    location.reload();
}


