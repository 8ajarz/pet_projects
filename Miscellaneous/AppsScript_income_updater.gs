// actSheet = is just an active sheet
// (start, end) - are starting and ending rows ot the edited range
// sources - list of values of courses of an income, located in B3:B7 
// s.getRange("B1").setValue(startRow+' to '+ endRow); - is just the code to show up variable I am interested in

let ss = SpreadsheetApp.getActiveSpreadsheet();
let s = ss.getActiveSheet();
let actSheetName = s.getSheetName(); // is need to determine in which column lies the cell with new income
let warningNote = "Это значение небыло учтено. В ячейках, выделенных красным, удали все, поставь заливку белым и, после этого, удали этот комментарий";

function rowIterator(actSheetName, rangeStart, rangeEnd, source){

  let startNum = 3; //Because income suorces start at 3d row
  let targCol = "D" 
  let incomeCOl = 0
  if (actSheetName === "расход"){
    incomeCOl = "F"
  } else if (actSheetName === "доход"){
    incomeCOl = "E"
  };

  for (var i = rangeStart; i <= rangeEnd; i++) {
    let indof = source.indexOf(s.getRange(incomeCOl + i).getValue()); //index of a cell of the income sources list
    if (indof < 0 || indof > 4){
      s.getRange(incomeCOl + i).setBackground("red");
      s.getRange(targCol + i).setBackground("red");
      s.getRange(targCol + i).setNote(warningNote);
      continue;
    };
    let num = Number(startNum) + Number(indof); 
    let targCell = "C" + num;
    let sum = Number(s.getRange(targCell).getValue()) + Number(s.getRange(targCol + i).getValue()); // sums up previous income and an income of a current cell in the loop
    s.getRange(targCell).setValue(sum); 
  };
  };


function onEdit(e) {
  var range = e.range;
  let startRow = range.getRow();
  let endRow = range.getLastRow();
  let firstRangeCol = range.getColumn();
  let lastRangeCol = range.getLastColumn();
  let vars = s.getRange("B3:B7").getValues().flat(); // creates the income sources list
  
  if (firstRangeCol <= 4 && lastRangeCol >= 4){ 
    rowIterator(actSheetName, startRow, endRow, vars);
  };
  
};

