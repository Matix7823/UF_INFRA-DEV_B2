const API_URL = 'http://localhost:5000/api';
let currentToken = null;
let currentPropertiesList = [];

// Images Premium
const propertyImages = [
    'assets/images/villa.png',
    'assets/images/apartment.png',
    'assets/images/penthouse.png'
];

function showResult(elementId, message, isSuccess = true) {
    const element = document.getElementById(elementId);
    if(!element) return;
    element.textContent = message;
    element.className = 'result ' + (isSuccess ? 'success' : 'error');
    element.style.display = 'block';
    setTimeout(() => { element.style.display = 'none'; }, 5000);
}

function updateUIForAuthenticatedUser(user) {
    const addProp = document.getElementById('add-property');
    const analytics = document.getElementById('analytics');
    const authForms = document.getElementById('auth-forms');
    const authTitle = document.getElementById('auth-title');
    const logoutBtn = document.getElementById('logout-container');
    
    if (addProp) addProp.style.display = 'block';
    if (analytics) analytics.style.display = 'block';
    if (authForms) authForms.style.display = 'none';
    if (authTitle) authTitle.textContent = `Espace VIP : ${user.nom}`;
    if (logoutBtn) logoutBtn.style.display = 'block';
    
    const vipBtn = document.getElementById('nav-vip-btn');
    if (vipBtn) {
        vipBtn.textContent = 'Mon Dashboard';
        vipBtn.style.background = 'var(--primary)';
        vipBtn.style.color = 'white';
        vipBtn.style.borderColor = 'var(--primary)';
    }

    // Si on est sur la page VIP, on charge les Analytics
    if(analytics) fetchAnalytics();
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.reload();
}

async function register() {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const nom = document.getElementById('register-nom').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, nom })
        });
        const data = await response.json();
        
        if (response.ok) {
            showResult('auth-result', '✓ Compte créé ! Connexion automatique en cours...', true);
            setTimeout(() => { login(email, password); }, 1500);
        } else {
            showResult('auth-result', '✗ ' + (data.error || 'Erreur'), false);
        }
    } catch (error) {
        showResult('auth-result', '✗ Serveur injoignable (Avez-vous bien lancé python app.py ?).', false);
    }
}

async function login(forcedEmail = null, forcedPassword = null) {
    let email = document.getElementById('login-email').value;
    let password = document.getElementById('login-password').value;
    
    if (typeof forcedEmail === 'string' && forcedEmail) email = forcedEmail;
    if (typeof forcedPassword === 'string' && forcedPassword) password = forcedPassword;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        
        if (response.ok) {
            currentToken = data.token;
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            updateUIForAuthenticatedUser(data.user);
        } else {
            showResult('auth-result', '✗ Identifiants réseau invalides', false);
        }
    } catch (error) {
        showResult('auth-result', '✗ Serveur hors-ligne (Avez-vous bien lancé python app.py ?).', false);
    }
}

async function fetchAnalytics() {
    try {
        const response = await fetch(`${API_URL}/analytics`);
        const data = await response.json();
        const kpiContainer = document.getElementById('kpi-container');
        if(!kpiContainer) return;

        if (response.ok) {
            let html = `
                <div class="kpi-card" style="animation: fadeUp 0.5s ease forwards">
                    <div class="kpi-label"><i class="fa-solid fa-house-flag"></i> Fonds de Commerce</div>
                    <div class="kpi-value">${data.total_properties} Unités</div>
                </div>
                <div class="kpi-card" style="animation: fadeUp 0.7s ease forwards">
                    <div class="kpi-label"><i class="fa-solid fa-chart-line"></i> Valeur Moyenne</div>
                    <div class="kpi-value">${Math.round(data.avg_price_sqm).toLocaleString('fr-FR')} €/m²</div>
                </div>
            `;
            
            const cities = data.cities_summary || {};
            let delay = 0.9;
            for (const [ville, stats] of Object.entries(cities)) {
                html += `
                    <div class="kpi-card" style="background:var(--light); color:var(--dark); box-shadow: var(--shadow-soft); animation: fadeUp ${delay}s ease forwards">
                        <div class="kpi-label" style="color:var(--text-muted); font-weight:600;">Tendance ${ville}</div>
                        <div class="kpi-value" style="font-size:2rem; color:var(--dark);">${Math.round(stats.price_per_sqm).toLocaleString('fr-FR')} €/m²</div>
                        <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.5rem;"><i class="fa-solid fa-key"></i> ${stats.count} mandats exclusifs</div>
                    </div>
                `;
                delay += 0.2;
            }
            kpiContainer.innerHTML = html;
        }
    } catch (error) {
        console.error('Erreur analytics:', error);
    }
}

// Interception de recherche depuis la Home Page pour rediriger vers portfolio.html
function handlePortfolioSearch(e) {
    if(e) e.preventDefault();
    const prixMin = document.getElementById('pf-prix-min')?.value || '';
    const prixMax = document.getElementById('pf-prix-max')?.value || '';
    const ville = document.getElementById('pf-ville')?.value || '';
    
    searchProperties(prixMin, prixMax, ville);
}

// Exécute la recherche réelle
async function searchProperties(pMin = '', pMax = '', pVille = '') {
    const list = document.getElementById('properties-list');
    const featuredList = document.getElementById('index-featured-list');
    
    // Si nous sommes sur l'accueil, on ne cible que le featured list.
    const targetElement = list || featuredList;
    if(!targetElement) return;

    let url = `${API_URL}/properties?`;
    if (pMin) url += `prix_min=${pMin}&`;
    if (pMax) url += `prix_max=${pMax}&`;
    if (pVille) url += `ville=${pVille}`;

    targetElement.innerHTML = '<div style="grid-column: 1/-1; text-align:center; color:var(--text-muted);"><i class="fa-solid fa-circle-notch fa-spin"></i> Collecte des données sécurisées...</div>';

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.properties || data.properties.length === 0) {
            targetElement.innerHTML = '<p class="section-desc" style="grid-column: 1/-1;">Aucune exclusivité ne matche avec vos critères.</p>';
            return;
        }

        currentPropertiesList = data.properties;
        
        // Sur l'accueil on ne montre que les 3 premiers
        const displayData = featuredList ? data.properties.slice(0, 3) : data.properties;

        targetElement.innerHTML = displayData.map((prop, idx) => {
            const imgPath = propertyImages[idx % propertyImages.length];
            const dpeClass = `dpe-${prop.dpe || 'A'}`;
            return `
            <div class="property-card" onclick="openModal(${idx}, '${imgPath}')" style="animation-delay: ${idx * 0.1}s">
                <div class="prop-img-wrapper">
                    <div class="prop-badge">${prop.status === 'disponible' ? 'Nouveauté' : 'Vendu'}</div>
                    <div class="dpe-tag ${dpeClass}">DPE: ${prop.dpe || 'A'}</div>
                    <img src="${imgPath}" alt="Photo de ${prop.titre}" loading="lazy">
                </div>
                <div class="prop-content">
                    <div class="prop-price">${prop.prix.toLocaleString('fr-FR')} €</div>
                    <h3 class="prop-title">${prop.titre}</h3>
                    <p style="color:var(--text-muted); font-size:0.95rem;">${prop.description.substring(0, 80)}...</p>
                    
                    <div class="prop-meta">
                        <span><i class="fa-solid fa-location-dot"></i> ${prop.ville}</span>
                        <span><i class="fa-solid fa-ruler-combined"></i> ${prop.surface} m²</span>
                        <span><i class="fa-solid fa-bed"></i> ${prop.chambres} Ch.</span>
                    </div>
                </div>
            </div>
        `}).join('');
    } catch (error) {
        targetElement.innerHTML = '<p class="section-desc" style="color:var(--danger)">Serveur Python hors-ligne ou erreur de base de données.</p>';
    }
}

async function createProperty() {
    if (!currentToken) return;

    const body = {
        titre: document.getElementById('prop-titre').value,
        prix: parseInt(document.getElementById('prop-prix').value),
        surface: parseInt(document.getElementById('prop-surface').value),
        chambres: parseInt(document.getElementById('prop-chambres').value),
        description: document.getElementById('prop-description').value,
        localisation: { ville: document.getElementById('prop-ville').value },
        dpe: document.getElementById('prop-dpe').value.toUpperCase() || 'A',
        equipements: ["Prestation Premium", "Domotique Avancée"]
    };

    try {
        const response = await fetch(`${API_URL}/properties`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify(body)
        });
        
        if (response.ok) {
            showResult('add-result', '✓ Mandat publié sur le réseau.', true);
            fetchAnalytics(); 
            document.querySelectorAll('#add-property input, #add-property textarea').forEach(e => e.value = '');
        } else {
            showResult('add-result', '✗ Champs Invalides', false);
        }
    } catch (error) {
        showResult('add-result', '✗ Erreur Système.', false);
    }
}


// ============== MODAL SYSTEM ==============

function openModal(idx, imgPath) {
    const prop = currentPropertiesList[idx];
    if(!prop) return;

    document.getElementById('modal-img').src = imgPath;
    document.getElementById('modal-price').textContent = `${prop.prix.toLocaleString('fr-FR')} €`;
    document.getElementById('modal-title').textContent = prop.titre;
    document.getElementById('modal-location-text').textContent = prop.ville;
    document.getElementById('modal-surface').textContent = `${prop.surface} m² hab.`;
    document.getElementById('modal-chambres').textContent = `${prop.chambres} Chambres`;
    document.getElementById('modal-desc').textContent = prop.description;
    
    const dpeBox = document.getElementById('modal-dpe');
    dpeBox.textContent = `DPE: ${prop.dpe || 'A'}`;
    dpeBox.className = `dpe-badge dpe-${prop.dpe || 'A'}`;

    let equips = [];
    try { equips = JSON.parse(prop.equipements); } catch(e) {}
    
    const ul = document.getElementById('modal-equip-list');
    if(equips && equips.length > 0) {
        ul.innerHTML = equips.map(eq => `<li>${eq}</li>`).join('');
    } else {
        ul.innerHTML = `<li>Service de Conciergerie</li><li>Prestations minimalistes luxe</li>`;
    }

    document.body.style.overflow = 'hidden';
    document.getElementById('property-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('property-modal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Fech modal on outside click
const modalEl = document.getElementById('property-modal');
if(modalEl) {
    modalEl.addEventListener('click', (e) => {
        if(e.target === modalEl) closeModal();
    });
}

// ============== INTERACTIONS ============== //

window.addEventListener('scroll', () => {
    const header = document.querySelector('.glass-header');
    if(!header) return;
    if (window.scrollY > 80) {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = 'var(--shadow-soft)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.85)';
        header.style.boxShadow = 'none';
    }
});

// Footer Newsletter
const btnNews = document.querySelector('.news-input button');
if(btnNews) {
    btnNews.addEventListener('click', (e) => {
        e.preventDefault();
        const input = document.querySelector('.news-input input');
        if(input.value) {
            input.value = "Merci pour votre inscription VIP !";
            input.disabled = true;
            setTimeout(() => {input.value=''; input.disabled=false;}, 3000);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    currentToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (currentToken && storedUser) {
        updateUIForAuthenticatedUser(JSON.parse(storedUser));
    }
    
    // Si on est sur la page Portfolio (présence de la recherche pf-ville ou URL avec query params form Homepage)
    const urlParams = new URLSearchParams(window.location.search);
    const pMin = urlParams.get('prix_min') || '';
    const pMax = urlParams.get('prix_max') || '';
    const pVille = urlParams.get('ville') || '';
    
    // On met à jour les champs de recherche si on vient de l'accueil
    const pfVilleInput = document.getElementById('pf-ville');
    if(pfVilleInput) {
        if(pMin) document.getElementById('pf-prix-min').value = pMin;
        if(pMax) document.getElementById('pf-prix-max').value = pMax;
        if(pVille) pfVilleInput.value = pVille;
    }
    
    // On charge les biens
    searchProperties(pMin, pMax, pVille);
});
