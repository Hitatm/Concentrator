function editCell(event){
	var currentCell;
	if(event == null){
		currentCell = window.event.srcElement;
	}else{
		currentCell = event.target;	
	}
	
	if(currentCell.tagName.toLowerCase() == "td"){
		var input = document.createElement("input");
        input.type = 'text';
        input.setAttribute('class', 'editable');
        input.value = currentCell.innerHTML;
        input.width = currentCell.style.width;
        
        input.onblur = function(){
            currentCell.innerHTML = input.value;
            //currentCell.removeChild(input);
        };
        input.onkeydown = function(event){
            if(event.keyCode == 13){
                input.blur();
            }
        };

        currentCell.innerHTML = '';
        currentCell.appendChild(input);
        input.focus();
	}	
}


