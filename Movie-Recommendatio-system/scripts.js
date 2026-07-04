function getFavorites() {
    return JSON.parse(localStorage.getItem("movie_favorites") || "[]");
}

function saveFavorites(favorites) {
    localStorage.setItem("movie_favorites", JSON.stringify(favorites));
}

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2200);
}

function addFavorite(button) {
    const card = button.closest(".movie-card");
    const title = card.dataset.title;
    const poster = card.dataset.poster;

    let favorites = getFavorites();

    const exists = favorites.some(movie => movie.title === title);

    if (exists) {
        showToast("Already saved ⭐");
        return;
    }

    favorites.push({
        title: title,
        poster: poster
    });

    saveFavorites(favorites);

    button.innerText = "Saved ✓";
    button.classList.add("saved");

    showToast("Movie saved to favorites ⭐");
}

function showFavorites() {
    const box = document.getElementById("favoriteBox");
    const list = document.getElementById("favoriteList");

    let favorites = getFavorites();

    box.style.display = "block";

    if (favorites.length === 0) {
        list.innerHTML = "<p>No favorite movies saved yet.</p>";
        showToast("No favorites found");
        return;
    }

    let html = "";

    favorites.forEach(movie => {
        html += `
            <div class="favorite-item">
                <img src="${movie.poster}" alt="${movie.title}">
                <strong>${movie.title}</strong>
            </div>
        `;
    });

    list.innerHTML = html;
    showToast("Favorite list loaded ⭐");
}

function clearFavorites() {
    localStorage.removeItem("movie_favorites");

    const list = document.getElementById("favoriteList");
    const box = document.getElementById("favoriteBox");

    list.innerHTML = "<p>Favorite list cleared.</p>";
    box.style.display = "block";

    document.querySelectorAll(".fav-btn").forEach(btn => {
        btn.innerText = "♡ Save";
        btn.classList.remove("saved");
    });

    showToast("Favorites cleared");
}

function openTrailer(button) {
    const card = button.closest(".movie-card");
    const title = card.dataset.title;

    const query = encodeURIComponent(title + " official trailer");
    window.open("https://www.youtube.com/results?search_query=" + query, "_blank");

    showToast("Opening trailer search 🎬");
}

function copyMovie(button) {
    const card = button.closest(".movie-card");
    const title = card.dataset.title;

    navigator.clipboard.writeText(title).then(() => {
        showToast("Movie name copied 📋");
    }).catch(() => {
        showToast("Copy failed");
    });
}

function markSavedCards() {
    const favorites = getFavorites();

    document.querySelectorAll(".movie-card").forEach(card => {
        const title = card.dataset.title;
        const button = card.querySelector(".fav-btn");

        const exists = favorites.some(movie => movie.title === title);

        if (exists) {
            button.innerText = "Saved ✓";
            button.classList.add("saved");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    markSavedCards();
});