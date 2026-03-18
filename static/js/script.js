<!DOCTYPE html>
<html>
<head>
    <title>Home</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>

<body>

<!-- Navbar -->
<nav class="navbar navbar-dark bg-transparent px-4">
    <span class="navbar-brand fw-bold">🎓 Grade Predictor</span>
    <div>
        <a href="/predict_page" class="btn btn-light me-2">Predict</a>
        <a href="/history" class="btn btn-warning">History</a>
    </div>
</nav>

<!-- Hero Section -->
<div class="hero d-flex flex-column justify-content-center align-items-center text-center">

    <h1 class="main-title">Student Grade Predictor</h1>
    <p class="subtitle">Smart predictions powered by Machine Learning</p>

    <a href="/predict_page" class="btn btn-glow mt-4">Get Started 🚀</a>

</div>

</body>
</html>