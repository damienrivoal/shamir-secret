// Implémentation DIY du secret de Shamir (schéma (k, n))
// Utilise l'arithmétique modulaire sur un petit nombre premier
// PHRASE TEST : je vais acheter des fraises rouges pour cuisiner une charlotte aux fraises mais il faudrait rajouter de la chantilly pour que ce soit divin

function mod(n, p) {
  return ((n % p) + p) % p;
}

// Conversion chaîne <-> tableau d'octets (UTF-8)
function stringToBytes(str) {
  return new TextEncoder().encode(str);
}
function bytesToString(bytes) {
  return new TextDecoder().decode(Uint8Array.from(bytes));
}

// Génère un polynôme aléatoire de degré (k-1) avec le secret comme terme constant
function generatePolynomial(secret, k, prime) {
  const coeffs = [secret];
  for (let i = 1; i < k; i++) {
    coeffs.push(Math.floor(Math.random() * prime));
  }
  return coeffs;
}

// Évalue le polynôme en x
function evalPolynomial(coeffs, x, prime) {
  let result = 0;
  for (let i = 0; i < coeffs.length; i++) {
    result = mod(result + coeffs[i] * Math.pow(x, i), prime);
  }
  return result;
}

// Génère n parts à partir d'un tableau d'octets (secretBytes)
function splitSecretString(secretStr, k, n, prime = 65537) {
  const secretBytes = stringToBytes(secretStr);
  // Pour chaque octet, on génère n parts
  // Chaque part est un tableau : [index, [octet1, octet2, ...]]
  const shares = Array.from({length: n}, (_, i) => [i+1, []]);
  for (let b = 0; b < secretBytes.length; b++) {
    const poly = generatePolynomial(secretBytes[b], k, prime);
    for (let i = 0; i < n; i++) {
      shares[i][1].push(evalPolynomial(poly, i+1, prime));
    }
  }
  return shares;
}

// Calcul de l'inverse modulaire (pour Lagrange)
function modInverse(a, p) {
  let t = 0, newT = 1;
  let r = p, newR = a;
  while (newR !== 0) {
    let quotient = Math.floor(r / newR);
    [t, newT] = [newT, t - quotient * newT];
    [r, newR] = [newR, r - quotient * newR];
  }
  if (r > 1) throw new Error('Non inversible');
  if (t < 0) t += p;
  return t;
}

// Interpolation de Lagrange en x=0
function lagrangeInterpolationAt0(points, prime) {
  let secret = 0;
  for (let i = 0; i < points.length; i++) {
    let [xi, yi] = points[i];
    let num = 1;
    let den = 1;
    for (let j = 0; j < points.length; j++) {
      if (i !== j) {
        let [xj, _] = points[j];
        num = mod(num * -xj, prime);
        den = mod(den * (xi - xj), prime);
      }
    }
    let li = mod(num * modInverse(den, prime), prime);
    secret = mod(secret + mod(yi * li, prime), prime);
  }
  return secret;
}

// Reconstitue le secret (chaîne) à partir de k parts
function recoverSecretString(shares, prime = 65537) {
  const len = shares[0][1].length;
  const secretBytes = [];
  for (let b = 0; b < len; b++) {
    const points = shares.map(([xi, yi]) => [xi, yi[b]]);
    const secret = lagrangeInterpolationAt0(points, prime);
    secretBytes.push(secret);
  }
  return bytesToString(secretBytes);
}

// Anciennes fonctions pour compatibilité (entier)
function splitSecret(secret, k, n, prime = 65537) {
  return splitSecretString(String.fromCharCode(secret), k, n, prime);
}
function recoverSecret(shares, prime = 65537) {
  const str = recoverSecretString(shares, prime);
  return str.charCodeAt(0);
}

// Exemple d'utilisation
const secret = 123; // Le secret à partager
const k = 3; // Nombre minimum de parts pour reconstituer
const n = 5; // Nombre total de parts
const prime = 257; // Un petit nombre premier > secret

const shares = splitSecret(secret, k, n, prime);
console.log('Parts générées :', shares);

// Pour reconstituer le secret, on prend n'importe quelles k parts
const selectedShares = shares.slice(0, k); // On prend les k premières pour l'exemple
const recovered = recoverSecret(selectedShares, prime);
console.log('Secret reconstitué :', recovered);

// === TEST AUTONOME ===
(function() {
  const phrase = "je vais acheter des fraises rouges pour cuisiner une charlotte aux fraises mais il faudrait rajouter de la chantilly pour que ce soit divin";
  const k = 3;
  const n = 5;
  const prime = 65537;
  console.log("Phrase originale :", phrase);
  const shares = splitSecretString(phrase, k, n, prime);
  console.log("Parts générées :", shares);
  // Prendre 3 parts quelconques (par exemple, 2, 4, 5)
  const selectedShares = [shares[1], shares[3], shares[4]];
  console.log("Parts utilisées pour décodage :", selectedShares.map(s => s[0]));
  const recovered = recoverSecretString(selectedShares, prime);
  console.log("Phrase reconstituée :", recovered);
  if (recovered === phrase) {
    console.log("\u2705 Succès : la phrase a été correctement reconstituée.");
  } else {
    console.error("\u274C Échec : la phrase reconstituée est différente !");
  }
})();
