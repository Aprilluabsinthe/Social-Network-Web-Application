var newVal = 0;
var prevVal = 0;
var prevOpr = '+';

function setNum(num){
    newVal = newVal * 10 + num;
    let display = document.getElementById('calc-display');
    display.value = String(newVal);
}

function preCal(){
    let result = 0;
    switch(prevOpr){
        case '+':
            result = prevVal + newVal;
            break;
        case '-':
            result = prevVal - newVal;
            break;
        case '*':
            result = prevVal * newVal;
            break;
        case '/':
            result = prevVal / newVal;
            break;
    }
    return parseInt(String(result));
    //return result;
}

function calculate(op){
    let result = preCal();
    let display = document.getElementById('calc-display');
    display.value = String(result);
    prevVal = result;
    prevOpr = op;
    newVal = 0;
}

function equals(op){
    let result = preCal();
    let display = document.getElementById('calc-display');
    display.value = String(result);
    prevVal = 0;
    prevOpr = '+';
    newVal = 0;
}


