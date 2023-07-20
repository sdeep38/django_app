function buildQuiz(){

    const output=[];

    Questions.forEach(
        (currentQuestion,questionNumber)=>{
            const answers=[];

            for(letter in currentQuestion.answers){
                answers.push(
                    `<label><input type="radio" name="question${questionNumber}" value="${letter}">${letter}:${currentQuestion.answers[letter]}</label>`
                );
            }
            output.push(
                `<div class="question">${currentQuestion.question}</div><div class="answers">${answers.join('')}</div>`
            );
        }
    );
    quizContainer.innerHTML=output.join('');

}

function showresults(){
    const answerContainers=quizContainer.querySelectorAll('.answers');

    let numCorrect=0;

    Questions.forEach(
        (currentQuestion,questionNumber)=>{
            const answerContainer=answerContainers[questionNumber];
            const Selector=`input[name=question${questionNumber}]:checked`;
            const userAnswer=(answerContainer.querySelector(Selector)||{}).value;

            if(userAnswer==currentQuestion.correctAnswer){
                numCorrect++;
                answerContainers[questionNumber].style.color='lightgreen';

            }else{
                answerContainers[questionNumber].style.color='red';
            }
        }
    );
    resultsContainer.innerHTML=`${numCorrect} out of ${Questions.length}`;

}

const quizContainer=document.getElementById('quiz');
const resultsContainer=document.getElementById('results');
const submitButton=document.getElementById('submit')
const Questions=[
    {
        question: "1) What is colour of an Apple?",
        answers:{
            a: "Red",
            b: "Blue",
            c: "Green"
        },
        correctAnswer: "a"
    },
    {
        question: "2) What is colour of Mango?",
        answers:{
            a: "Red",
            b: "Yellow",
            c: "Green"
        },
        correctAnswer: "b"
    },
    {
        question: "3) What is colour of Tulsi leaves?",
        answers:{
            a: "Red",
            b: "Blue",
            c: "Green"
        },
        correctAnswer: "c"
    }

];

buildQuiz(Questions,quizContainer);

submitButton.addEventListener('click',showresults);