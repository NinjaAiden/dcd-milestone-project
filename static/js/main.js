function createIngredient() {
    var ingredientInput = document.getElementById('ingredient_field').value;
    var ing = document.createElement("input");
    ing.setAttribute('name', 'ingredient');
    ing.setAttribute('type', 'text');
    ing.setAttribute('class', 'col-11 my-1');
    ing.setAttribute('value', ingredientInput);
    var newLine = document.createElement("br");
    var element = document.getElementById("ingredient_outer");
    element.appendChild(ing);
    element.appendChild(newLine);
    document.getElementById("ingredient_field").value = "";
}

function createMethod() {
    var methodInput = document.getElementById('method_field').value;
    var met = document.createElement("input");
    met.setAttribute('name', 'method');
    met.setAttribute('type', 'text');
    met.setAttribute('class', 'col-11 my-1');
    met.setAttribute('value', methodInput);
    var newLine = document.createElement("br");
    var element = document.getElementById("method_outer");
    element.appendChild(met);
    element.appendChild(newLine);
    document.getElementById("method_field").value = "";
}

function confirmDelete() {
    var confirmBtn = document.getElementById("confirmDeleteBtn");
    if (confirmBtn.style.display === "none") {
        confirmBtn.style.display = "block";
    }
    else {
        confirmBtn.style.display = "none";
    }
}
