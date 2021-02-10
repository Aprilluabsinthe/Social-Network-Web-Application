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
    let err = false;
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
    return result;
    //return result;
}

function reset(result,op,nv){
    prevVal = result;
    prevOpr = op;
    newVal = nv;
    displayPara();
}

function clear(){
    prevVal = 0;
    prevOpr = '+';
    newVal = 0;
    displayPara();
}

function displayPara(){
    document.getElementById('prevval').value = parseInt(String(prevVal));
    document.getElementById('prevop').value = prevOpr;
}

function calculate(op){
    let result = preCal();
    if(isNaN(result) || result === Infinity){
        clear();
        alert("Error: your input contains illegal /0, computation turns to " + result);
    }
    else{
        let display = document.getElementById('calc-display');
        display.value = parseInt(String(result));
        displayPara();
        reset(result,op,0);
    }
}

function equals(){
    let result = preCal();
    if( isNaN(result) || result===Infinity){
        alert("Error: your input contains illegal /0, computation turns to " + result);
    }
    else{
        let display = document.getElementById('calc-display');
        display.value = display.value = parseInt(String(result));
        displayPara();
    }
    clear();
}


