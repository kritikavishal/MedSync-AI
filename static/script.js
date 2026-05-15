async function submitData(){

    const name = document.getElementById("name").value

    const symptoms = document.getElementById("symptoms").value

    const phone = document.getElementById("phone").value

    const response = await fetch("/submit",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            name:name,
            symptoms:symptoms,
            phone:phone
        })
    })

    const data = await response.json()

    if(data.error){

        document.getElementById("result").innerHTML =
        `
        <div class="result-card">
            <h2>Error</h2>
            <div class="result-box emergency-status">
                ${data.error}
            </div>
        </div>
        `
    }

    else{

        let statusClass = "normal-status"

        if(data.urgency >= 90){
            statusClass = "emergency-status"
        }

        document.getElementById("result").innerHTML =

        `
        <div class="result-card">

            <h2>AI Medical Summary</h2>

            <div class="result-box">
                <div class="result-title">Urgency Score</div>
                <div class="result-value">${data.urgency}</div>
            </div>

            <div class="result-box ${statusClass}">
                <div class="result-title">Patient Status</div>
                <div class="result-value">${data.alert}</div>
            </div>

            <div class="result-box">
                <div class="result-title">AI Recommendation</div>
                <div class="ai-summary">
                    ${data.recommendation}
                </div>
            </div>

        </div>
        `
    }
}