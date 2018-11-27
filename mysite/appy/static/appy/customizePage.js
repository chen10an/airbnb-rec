function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    const div = ev.dataTransfer.getData("text");
  	const pointA = document.getElementById(div);
  	const currHTML = ev.target.innerHTML;
    ev.target.innerHTML = "";
    // if (ev.target.id == "farleft") {
    // 	ev.target.innerHTML+=(currHTML+"<br\>");
    // }
    ev.target.appendChild(pointA);
    ev.target.setAttribute("style", "padding-top: 2vh");
    console.log(pointA.id)
    console.log(pointA.parentNode.id);
}
