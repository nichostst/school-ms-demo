var clicks = 0;

document.getElementById("add_button").onclick = function () {
    clicks += 1;
    if (clicks < 8) {
    const container = document.getElementById('structure_container');
    const child = `
    <div class="row" id="structure_child" style="margin-bottom: 0; display: flex; align-items: center;">
      <div class="input-field col">
        <select class="structure_type" name="type_${ clicks + 1 }" style="font-size: 11pt; margin-top: -18pt;">
          <option value="" disabled selected>Choose type</option>
          <option value="Assignment">Assignment</option>
          <option value="Exam">Exam</option>
          <option value="Project">Project</option>
        </select>
      </div>
      <div class="input-field col s6">
        <input class="structure_name" name="structure_${ clicks + 1 }" type="text">
        <label>Structure Name</label>
      </div>
      <div class="input-field col s2">
        <input class="weightage" name="weight_${ clicks + 1 }" type="number" min="5">
        <label>Weight (%)</label>
      </div>
    </div>`
    container.insertAdjacentHTML(
        'beforeend', child
    )
    } else {
    const status = document.getElementById('create_status_info')
    status.style.visibility = "visible"
    status.innerText = 'Maximum number of structures (max: 8) reached!'
    }
}