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

function calculate(op){
    let result = preCal();
    if(isNaN(result) || result===Infinity){
        prevVal = 0;
        prevOpr = '+';
        newVal = 0;
        alert("Error: your input contains illegal /0, computation turns to " + result);
    }
    else{
        let display = document.getElementById('calc-display');
        prevVal = result;
        prevOpr = op;
        newVal = 0;
        display.value = parseInt(String(result));
    }

}

function equals(op){
    let result = preCal();
    if( isNaN(result) || result===Infinity){
        prevVal = 0;
        prevOpr = '+';
        newVal = 0;
        alert("Error: your input contains illegal /0, computation turns to " + result);
    }
    else{
        let display = document.getElementById('calc-display');
        display.value = display.value = parseInt(String(result));
        prevVal = 0;
        prevOpr = '+';
        newVal = 0;
    }

}


