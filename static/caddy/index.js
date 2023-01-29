
    const servers = [
        "http://localhost",
        "http://127.0.0.1",
        "https://87ff-89-64-1-231.eu.ngrok.io"
    ];
    const ports = ["", ":8000", ":2019"];
    const resources = ["/", "/time.html"];

    let el = "";
    for (let s in servers) {
        for (let p in ports) {
            for (let r in resources) {
                    el += "<a href='"
                        + servers[s] 
                        + ports[p]
                        + resources[r]
                        + "'>"
                        + servers[s]
                        + ports[p]
                        + resources[r]
                        + "<a><br/>"
            }
        }
    }
    
    document.getElementById("server-list").innerHTML = el;
