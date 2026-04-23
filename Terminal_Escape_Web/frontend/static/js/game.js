let currentSessionId = null;
let map = null;
let currentMarker = null;
let safeMarker = null;

function initMap() {
    map = L.map('map').setView([32, 53], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);
}

function updateMap(current, safe) {
    if (!map) return;
    if (currentMarker) map.removeLayer(currentMarker);
    if (safeMarker) map.removeLayer(safeMarker);

    currentMarker = L.marker([current.latitude_deg, current.longitude_deg], {
        icon: L.divIcon({className: 'bg-red-600 text-white w-8 h-8 flex items-center justify-center rounded-full', html: '📍'})
    }).addTo(map).bindPopup(`<b>Current Location:</b><br>${current.name}`);

    safeMarker = L.marker([safe.latitude_deg, safe.longitude_deg], {
        icon: L.divIcon({className: 'bg-emerald-600 text-white w-8 h-8 flex items-center justify-center rounded-full', html: '🏁'})
    }).addTo(map).bindPopup(`<b>Safe Airport:</b><br>${safe.name}`);

    map.fitBounds([[current.latitude_deg, current.longitude_deg], [safe.latitude_deg, safe.longitude_deg]], {padding: [50, 50]});
}

function updateStatus(state) {
    document.getElementById('gameStatus').innerHTML = `
        <div class="grid grid-cols-2 gap-4 text-sm">
            <div>Round: <span class="font-bold text-emerald-400">${state.round}</span></div>
            <div>Money: <span class="font-bold">$${state.money.toLocaleString()}</span></div>
            <div>CO₂: <span class="font-bold">${state.co2}</span></div>
            <div>Distance to Safe: <span class="font-bold">${state.distance_to_safe_km} km</span></div>
            <div>Police Risk: <span class="font-bold text-red-400">${state.police_chance_percent}%</span></div>
            <div>Safe Flight Chance: <span class="font-bold text-emerald-400">${state.flight_availability_percent}%</span></div>
        </div>
    `;
}

function showFlights(flights) {
    const container = document.getElementById('flightsList');
    container.innerHTML = '<p class="text-gray-400 mb-4 font-medium">Available Flights:</p>';

    flights.forEach(flight => {
        const moneyCost = Math.floor(Math.random() * 1400) + 450;
        const co2Cost = Math.floor(moneyCost * 0.4);

        const div = document.createElement('div');
        div.className = 'flight-option bg-gray-800 hover:bg-gray-700 p-6 rounded-3xl cursor-pointer border border-gray-700';
        div.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <div class="font-semibold">${flight.name}</div>
                    <div class="text-xs text-gray-400">${flight.ident}</div>
                </div>
                <div class="text-right">
                    <div class="text-emerald-400 font-bold text-2xl">$${moneyCost}</div>
                    <div class="text-orange-400">${co2Cost} CO₂</div>
                </div>
            </div>
        `;
        div.onclick = () => makeMove(flight.ident);
        container.appendChild(div);
    });
}

async function makeMove(selectedIdent) {
    const res = await fetch('/api/game/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ session_id: currentSessionId, selected_ident: selectedIdent })
    });
    const data = await res.json();

    if (data.success) {
        if (data.game_over) {
            const msg = data.result === 'won' ? "🎉 Congratulations! You reached the safe airport!" :
                        data.result === 'caught' ? "💀 You were caught by the police!" : "💀 You ran out of resources!";
            alert(msg + `\n\nRounds played: ${data.game_state.round}`);
            window.location.href = 'index.html';
            return;
        }

        currentSessionId = data.game_state.session_id;
        updateStatus(data.game_state);
        showFlights(data.available_flights);
        updateMap(data.game_state.current_airport, data.game_state.safe_airport);
    } else {
        alert(data.error || "An error occurred");
    }
}

function showLeaderboards() {
    window.location.href = 'leaderboard.html';
}

function quitGame() {
    if (confirm("Are you sure you want to quit the game? Your progress will be saved.")) {
        alert("✅ Game saved. Thank you for playing!");
        window.location.href = 'index.html';
    }
}

window.onload = async () => {
    const player = JSON.parse(localStorage.getItem('player'));
    if (!player) return window.location.href = 'index.html';

    document.getElementById('playerInfo').innerHTML = `Player: <span class="text-emerald-400">${player.player_name}</span>`;

    initMap();

    let res = await fetch('/api/game/continue', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ player_id: player.player_id })
    });
    let data = await res.json();

    if (!data.success) {
        res = await fetch('/api/game/new', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ player_id: player.player_id })
        });
        data = await res.json();
    }

    if (data.success) {
        currentSessionId = data.session_id || data.game_state.session_id;
        updateStatus(data.game_state);
        showFlights(data.available_flights);
        updateMap(data.game_state.current_airport, data.game_state.safe_airport);
    }
};