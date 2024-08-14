document.addEventListener('DOMContentLoaded', (event) => {

    // Check the action type in formContents and trigger the appropriate button click
    if (formContents.action === 'explore') {
        document.querySelector('.expBtn').click();
        document.querySelector('.regex').value = formContents.regex;
        console.log("exp showed")
    } else {
        document.querySelector('.anaBtn').click();
        console.log("ana showed")
    }

    var textNames = document.querySelectorAll('.show-text');
    var toShow = document.querySelectorAll('.showed-text');

    // Toggle visibility of text sections when clicked
    for (let i = 0; i < textNames.length; i++) {
        textNames[i].addEventListener('click', function() {
            console.log("clicked")
            if (toShow[i].style.display === 'block') {
                toShow[i].style.display = 'none';
            } else {
                toShow[i].style.display = 'block';
            };
        });
    };

    function disableSecondInput() {
        // Disable one input if the other has content
        var fileInput = document.getElementById('fileInput');
        var textInput = document.getElementById('textInput');

        if (fileInput.files.length !== 0) {
            textInput.disabled = true;
            fileInput.disabled = false;
        }
        else if (textInput.value.trim() !== '') {
            fileInput.disabled = true;
            textInput.disabled = false;
        } else {
            fileInput.disabled = false;
            textInput.disabled = false;
        };
    };

    // Add event listeners to file and text inputs to disable the other input if one is filled
    document.getElementById('fileInput').addEventListener('change', disableSecondInput);
    document.getElementById('textInput').addEventListener('input', disableSecondInput);

    disableSecondInput();
});

function setActionColor(action, buttonClass) {
    // Set the value of the action and update the active button's color and visibility of regex field
    document.querySelector('.action').value = action;

    document.querySelector('.anaBtn').classList.remove('active-button');
    document.querySelector('.expBtn').classList.remove('active-button');
    document.querySelector(buttonClass).classList.add('active-button');

    // Show or hide the regex field based on the selected action
    var regex = document.querySelector('.regexField');
    if (buttonClass === '.expBtn') {
        regex.style.display = 'flex';
        regex.style.justifyContent = 'center';
    } else {
        regex.style.display = 'none';
    };
};

function showNameInput(element) {
    // Display the name input field
    document.querySelector(element).style.display = 'flex';
}

function hideWindow(element) {
    // Hide the specified window or element
    document.querySelector(element).style.display = 'none';
};

function submitTextId(sqlId, inputId) {
    // Set the SQL user ID of file to be searched through or deleted
    var textId = document.getElementById(inputId);
    textId.value = sqlId;
}

function submitForm() {
    // Submit form
    document.getElementById('user-form').submit();
}

function searchFilter() {
    // Filter table rows based on search input (borrowed from https://www.w3schools.com/howto/howto_js_filter_lists.asp)
    var input = document.getElementById("search-filter");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("sortable");
    var tr = table.getElementsByTagName("tr");
  
    // Loop through table rows and hide those that don't match the filter
    for (let i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            var txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            };
        };
    };
};

function makeHistogram(lengths, graphId, type, binSize) {
    // Create a histogram using Plotly
    var trace = {
        x: lengths,
        type: 'histogram',
        marker: {
            color: "rgb(255, 159, 253)", 
            line: {
              color: "rgb(198, 87, 197)", 
              width: 2
            }
        },  
        opacity: 0.8, 
        xbins: {size: binSize}
    };

    var layout = {
        plot_bgcolor: "rgb(0, 0, 0, 0)",
        paper_bgcolor: "rgb(0, 0, 0, 0)",
        title: `${type} lengths histogram`,
        xaxis: {title: `${type} length`},
        yaxis: {title: `${type} count`},
        bargap: 0.05,
        font: {
            color: 'white'
        }
    };

    var data = [trace];
    Plotly.newPlot(graphId, data, layout);
};


function makeScattPlot(lengths, graphId) {
    // Create a scatter plot to show sentence length progression using Plotly
    var trace = {
        x: [...Array(lengths.length).keys()],
        y: lengths,
        mode: 'lines+markers',
        type: 'scatter',
        marker: {
            color: "rgb(255, 159, 253)"
        }
    }

    var layout = {
        plot_bgcolor: "rgb(0, 0, 0, 0)",
        paper_bgcolor: "rgb(0, 0, 0, 0)",
        title: 'Progression of sentence lengths',
        xaxis: {title: 'Sentence index'},
        yaxis: {title: 'Sentence length'},
        font: {
            color: 'white'
        }
    };

    var data = [trace];
    Plotly.newPlot(graphId, data, layout);
};


function saveTableCSV(table_id, separator = ",") {
    // Convert an HTML table to a CSV file and trigger download 
    // (borrowed from https://dev.to/popoolatopzy/how-to-convert-html-table-to-csv-file-14p3)

    // Select rows from table_id
    var rows = document.querySelectorAll("table#" + table_id + " tr");
    // Construct csv
    var csv = [];
      //looping through the table
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
           //looping through the tr
        for (var j = 0; j < cols.length; j++) {
           // removing space from the data
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, "").replace(/(\s\s)/gm, " ")
             // removing double qoute from the data
            data = data.replace(/"/g, `""`);
            // Push escaped string
            row.push(`"` + data + `"`);
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join("\n");
    // Download it
    var filename = "export_" + table_id + "_" + new Date().toLocaleDateString() + ".csv";
    var link = document.createElement("a");
    link.style.display = "none";
    link.setAttribute("target", "_blank");
    link.setAttribute("href", "data:text/csv;charset=utf-8," + encodeURIComponent(csv_string));
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}