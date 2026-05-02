let currentSessionId = null;
let map = null;

let currentMarker = null;
let safeMarker = null;
let routeLine = null;



/* ===================== BACKGROUND ===================== */

const bgImage = document.getElementById("bg-image");

function changeBG(src) {
    if (!bgImage) return;

    bgImage.style.opacity = 0;

    setTimeout(() => {
        bgImage.src = src;
        bgImage.style.opacity = 0.85;
    }, 200);
}

function setIdleBG() {
    changeBG("images/1.jpg"); // عکس عادی
}

function setSelectedBG() {
    changeBG("images/2.jpeg"); // عکس کلیک
}
/* ===================== MAP ===================== */

function initMap() {
    map = L.map('map').setView([30, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);
}

function updateMap(current, safe) {
    if (!map) return;

    if (currentMarker) map.removeLayer(currentMarker);
    if (safeMarker) map.removeLayer(safeMarker);
    if (routeLine) map.removeLayer(routeLine);

    currentMarker = L.marker([current.latitude_deg, current.longitude_deg])
        .addTo(map)
        .bindPopup("📍 " + current.name);

    safeMarker = L.marker([safe.latitude_deg, safe.longitude_deg])
        .addTo(map)
        .bindPopup("🏁 " + safe.name);

    routeLine = L.polyline(
        [
            [current.latitude_deg, current.longitude_deg],
            [safe.latitude_deg, safe.longitude_deg]
        ],
        {
            color: "cyan",
            weight: 4,
            opacity: 0.8,
            dashArray: "10,10"
        }
    ).addTo(map);

    map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
}

/* ===================== UI STATUS ===================== */

function updateStatus(state) {
    document.getElementById('gameStatus').innerHTML = `
        <div class="grid grid-cols-2 gap-3 text-sm">

            <div>Round: <span class="text-emerald-400 font-bold">${state.round}</span></div>
            <div>Money: <span class="text-yellow-400 font-bold">$${state.money}</span></div>
            <div>CO₂: <span class="text-orange-400 font-bold">${state.co2}</span></div>

            <div>From: <span class="text-red-400">${state.current_airport.name}</span></div>
            <div>To: <span class="text-emerald-400">${state.safe_airport.name}</span></div>

            <div>Police Risk: <span class="text-red-500">${state.police_chance_percent}%</span></div>
            <div>Flight Chance: <span class="text-blue-400">${state.flight_availability_percent}%</span></div>

        </div>
    `;
}

/* ===================== FLIGHTS ===================== */

function showFlights(flights) {
    const container = document.getElementById('flightsList');
    container.innerHTML = "";

    flights.forEach(f => {
        const div = document.createElement("div");

        div.className = "bg-gray-800 p-4 rounded-xl cursor-pointer hover:bg-gray-700 transition";
        div.innerHTML = `✈️ ${f.name}`;

        div.onclick = () => makeMove(f.ident);

        container.appendChild(div);
    });
}

/* ===================== AIRPLANE FX ===================== */

function airplaneFX() {
    const plane = document.getElementById("planeHUD");

    if (!plane) return;

    plane.classList.remove("fly");
    void plane.offsetWidth;
    plane.classList.add("fly");
}

/* ===================== POLICE CINEMATIC ===================== */

async function policeScan() {

    setSelectedBG()

    return new Promise(resolve => {

        let i = 0;

        const overlay = document.createElement("div");
        overlay.className = "ai-overlay";
        overlay.innerText = "🚓 AI Searching... 0/10";

        document.body.appendChild(overlay);

        const interval = setInterval(() => {

            overlay.innerText = `🚓 AI Searching... ${i}/10`;
            i++;

            if (i > 10) {
                clearInterval(interval);
                overlay.remove();
                resolve();
            }

        }, 300);
    });
}

/* ===================== MAIN MOVE ===================== */

async function makeMove(selectedIdent) {
    setSelectedBG();
    

    // ✈️ + 🚓 cinematic start
    airplaneFX();
    await policeScan();

    const res = await fetch('/api/game/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: currentSessionId,
            selected_ident: selectedIdent
        })
    });

    const data = await res.json();

    if (!data.success) {
        alert(data.error || "Error");
        return;
    }

    /* ===================== GAME OVER ===================== */

    if (data.game_over) {

        /* ===================== CAUGHT BY AI ===================== */
        if (data.result === "caught") {
    
            const overlay = document.createElement("div");
    
            overlay.className = `
                fixed inset-0 bg-black flex flex-col items-center justify-center text-center z-50
            `;
    
            overlay.innerHTML = `
                <div class="text-red-500 text-6xl mb-4 animate-pulse">🚓 CAUGHT</div>
    
                <div class="text-white text-2xl mb-6">
                    You have been detected by the AI surveillance system.
                </div>
    
                <div class="text-gray-300 mb-6">
                    Your flight path was analyzed...  
                    <br>
                    Escape attempt failed.
                </div>
    
                <div class="text-red-400 text-xl mb-8">
                    “Resistance is futile.”
                </div>
    
                <button onclick="window.location.href='menu.html'"
                    class="bg-red-600 px-8 py-3 rounded-2xl">
                    Back to Safe House
                </button>
            `;
            
            document.body.appendChild(overlay);
    
            return;
        }
    
        /* ===================== WIN ===================== */
        else if (data.result === "won") {
    
            const overlay = document.createElement("div");
    
            overlay.className = `
                fixed inset-0 bg-black flex flex-col items-center justify-center text-center z-50
            `;
    
            overlay.innerHTML = `
                <div class="text-6xl mb-4">🏁 MISSION COMPLETE</div>
    
                <div class="text-emerald-400 text-2xl mb-6">
                    You successfully escaped the AI surveillance system.
                </div>
    
                <div class="text-gray-300 mb-6">
                    Humanity’s last hope has reached safety.
                    <br>
                    The resistance chip has been delivered.
                </div>
    
                <div class="text-yellow-400 text-xl mb-8">
                    ✈️ Well flown, pilot.
                </div>
    
                <button onclick="window.location.href='menu.html'"
                    class="bg-emerald-600 px-8 py-3 rounded-2xl text-white">
                    Return to Base
                </button>
            `;
    
            document.body.appendChild(overlay);
    
            return;
        }
    
        /* ===================== RESOURCE LOSS ===================== */
        else if (data.result === "lost_resources") {
    
            const overlay = document.createElement("div");
    
            overlay.className = `
                fixed inset-0 bg-black flex flex-col items-center justify-center text-center z-50
            `;
    
            overlay.innerHTML = `
                <div class="text-yellow-500 text-6xl mb-4">💥 CRASHED</div>
    
                <div class="text-white text-2xl mb-6">
                    Your aircraft ran out of resources mid-flight.
                </div>
    
                <div class="text-gray-300 mb-6">
                    Fuel / CO₂ / Budget exhausted.<br>
                    The journey ended prematurely.
                </div>
    
                <div class="text-yellow-400 text-xl mb-8">
                    “No fuel. No future.”
                </div>
    
                <button onclick="window.location.href='menu.html'"
                    class="bg-yellow-600 px-8 py-3 rounded-2xl">
                    Try Again
                </button>
            `;
    
            document.body.appendChild(overlay);
    
            return;
        }
    
        return;
    }

    /* ===================== CONTINUE GAME ===================== */

    currentSessionId = data.game_state.session_id;

    updateStatus(data.game_state);
    showFlights(data.available_flights);
    updateMap(data.game_state.current_airport, data.game_state.safe_airport);

    setIdleBG();
}

/* ===================== MENU ===================== */

function showLeaderboards() {
    window.location.href = "leaderboard.html";
}

function quitGame() {
    window.location.href = "menu.html";
}

function story(){
    document.getElementById("storyModal").classList.remove("hidden");
    document.getElementById("storyModal").classList.add("flex");
}

function closeStory(){
    document.getElementById("storyModal").classList.add("hidden");
    document.getElementById("storyModal").classList.remove("flex");
}
/* ===================== INIT ===================== */

window.onload = async () => {

    const player = JSON.parse(localStorage.getItem("player"));

    if (!player) {
        window.location.href = "index.html";
        return;
    }

    initMap();
    setIdleBG();


    let res = await fetch('/api/game/continue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: player.player_id })
    });

    let data = await res.json();

    if (!data.success) {

        res = await fetch('/api/game/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: player.player_id })
        });

        data = await res.json();
    }

    currentSessionId = data.session_id || data.game_state.session_id;

    updateStatus(data.game_state);
    showFlights(data.available_flights);
    updateMap(data.game_state.current_airport, data.game_state.safe_airport);
};