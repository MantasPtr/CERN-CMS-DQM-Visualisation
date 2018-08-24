function onFetchData(){
    let runValue =  getStringValueFromInputField("runInput");
    if (!runValue){
        showApiError("Empty RUN input value");
    }

    fetch("/fetch/" + runValue).then(
        (response) => {
            if (validateApiResponseCode(response)) {
                showApiMessage("Fetching for run: " + runValue +  " initialized!")
            }
        }
    );
}

function deleteRun(identifier){
    fetch("/data/" + identifier.run, {
        method:"DELETE"
    }).then(
        (response) => { 
            validateResponseCode(response);
            showApiMessage("Deleted " +response.text + "file")
        }
    )
};