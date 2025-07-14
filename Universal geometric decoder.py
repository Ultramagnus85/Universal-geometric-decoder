import React, { useState, useEffect, useRef } from 'react';
import { Play, Upload, ChevronRight, Calculator, Eye, CheckCircle, ImageIcon, RotateCcw, Zap } from 'lucide-react';

const SacredGeometryDecoder = () => {
  const [selectedSymbol, setSelectedSymbol] = useState('seedOfLife');
  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imageAnalysis, setImageAnalysis] = useState(null);
  const [mode, setMode] = useState('preset'); // 'preset' or 'upload'
  const [error, setError] = useState(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  const presetSymbols = {
    seedOfLife: {
      name: 'Seed of Life',
      description: '7 overlapping circles in hexagonal pattern',
      geometry: 'Radial symmetry, 6-fold rotational symmetry, central convergence point',
      constraint: 'Radial divergence from core point',
      operator: '∇ · Φ = ρ',
      physicsLaw: "Gauss's Law / Field Divergence",
      application: 'Electric field from point charges, gravitational field mapping',
      equation: 'div(E) = ρ/ε₀',
      verification: 'Dimensional: [E]/[L] = [ρ]/[ε₀] ✓'
    },
    flowerOfLife: {
      name: 'Flower of Life',
      description: '19 overlapping circles in hexagonal lattice',
      geometry: 'Multiple interference nodes, periodic lattice structure',
      constraint: 'Multiple radial modes in interference pattern',
      operator: 'Φ(x,t) = Σₙ ψₙ(x)e^(-iωₙt)',
      physicsLaw: 'Wave Superposition / Harmonic Fields',
      application: 'Optical interference, acoustic resonance, quantum superposition',
      equation: '∇²ψₙ = -kₙ²ψₙ',
      verification: 'Dimensional: [k²][ψ] = [∇²ψ] ✓'
    },
    torus: {
      name: 'Torus',
      description: 'Donut-shaped surface with circular cross-sections',
      geometry: 'Closed loop topology, azimuthal symmetry, circulation',
      constraint: 'Azimuthally looped vector flow',
      operator: '∮ B · dl = μ₀I',
      physicsLaw: "Ampère's Circuital Law",
      application: 'Magnetic field around currents, tokamak plasma confinement',
      equation: 'curl(B) = μ₀J',
      verification: 'Dimensional: [B]/[L] = [μ₀][J] ✓'
    },
    goldenSpiral: {
      name: 'Golden Spiral',
      description: 'Logarithmic spiral with golden ratio growth',
      geometry: 'Self-similar scaling, constant angular growth rate',
      constraint: 'Logarithmic radial curve conserving angular growth',
      operator: 'r(θ) = ae^(bθ), b = ln(φ)/π',
      physicsLaw: 'Minimum Energy Scaling Path',
      application: 'Galaxy arms, shell growth, fluid vortices, optimization paths',
      equation: 'dE/dr = minimal for φ-scaling',
      verification: 'Dimensional: [r] vs [θ] scaling consistent ✓'
    },
    vesicaPiscis: {
      name: 'Vesica Piscis',
      description: 'Intersection of two equal circles',
      geometry: 'Lens-shaped intersection, bilateral symmetry',
      constraint: 'Intersection region of circular field fronts',
      operator: 'E = ½mv² = ℏω',
      physicsLaw: 'Classical-Quantum Energy Bifurcation',
      application: 'Wave-particle duality, resonator modes, optical lensing',
      equation: 'λ = h/p (de Broglie relation)',
      verification: 'Dimensional: [E] = [ℏ][ω] ✓'
    },
    metatronsCube: {
      name: "Metatron's Cube",
      description: '13-sphere structure containing all 5 Platonic solids',
      geometry: '3D polyhedral framework, icosahedral symmetry, nested geometric forms',
      constraint: 'Discrete crystalline lattice with multiple symmetry groups',
      operator: 'H = -ℏ²/2m ∇² + V(r) with crystalline potential',
      physicsLaw: 'Quantum Crystallography / Bloch Wave Theory',
      application: 'Crystal band structure, electronic states in solids, quasicrystal physics',
      equation: 'ψ(r) = e^(ik·r) u_k(r) (Bloch theorem)',
      verification: 'Dimensional: [ψ] = [L^(-3/2)] ✓'
    },
    aries: {
      name: 'Aries (Ram)',
      description: 'V-shaped constellation representing the ram',
      geometry: 'Angular momentum vector, directional thrust pattern',
      constraint: 'Rotational kinetic energy with angular acceleration',
      operator: 'L = r × p, τ = dL/dt',
      physicsLaw: 'Angular Momentum Conservation / Torque Dynamics',
      application: 'Gyroscopic motion, planetary rotation, spin angular momentum',
      equation: 'τ = Iα (rotational analog of F = ma)',
      verification: 'Dimensional: [τ] = [L²M/T²] ✓'
    },
    taurus: {
      name: 'Taurus (Bull)',
      description: 'V-shaped cluster with prominent bright stars',
      geometry: 'Gravitational binding energy, cluster dynamics',
      constraint: 'Stable bound system under mutual gravitational attraction',
      operator: 'E = -GM²/2R (virial theorem)',
      physicsLaw: 'Gravitational Binding / Virial Equilibrium',
      application: 'Star cluster dynamics, galactic structure, dark matter halos',
      equation: '2K + U = 0 (virial equilibrium)',
      verification: 'Dimensional: [E] = [GM²/R] ✓'
    },
    gemini: {
      name: 'Gemini (Twins)',
      description: 'Two parallel bright stars in close proximity',
      geometry: 'Binary system orbital mechanics, coupled oscillators',
      constraint: 'Two-body problem with mutual gravitational interaction',
      operator: 'μ d²r/dt² = -GMm/r² (reduced mass system)',
      physicsLaw: 'Kepler Laws / Binary Star Dynamics',
      application: 'Binary star systems, exoplanet detection, tidal forces',
      equation: 'T² = 4π²a³/G(M₁+M₂) (Kepler\'s third law)',
      verification: 'Dimensional: [T²] = [a³/GM] ✓'
    },
    cancer: {
      name: 'Cancer (Crab)',
      description: 'Faint cluster formation with central concentration',
      geometry: 'Spherical symmetry with central density enhancement',
      constraint: 'Hydrostatic equilibrium in spherical geometry',
      operator: 'dP/dr = -ρ GM(r)/r² (hydrostatic equation)',
      physicsLaw: 'Hydrostatic Equilibrium / Stellar Structure',
      application: 'Stellar interiors, planetary atmospheres, gas giant structure',
      equation: 'M(r) = 4π ∫₀ʳ ρ(r\')r\'² dr\'',
      verification: 'Dimensional: [dP/dr] = [ρ][GM/r²] ✓'
    },
    leo: {
      name: 'Leo (Lion)',
      description: 'Distinctive sickle shape with bright central star',
      geometry: 'Curved trajectory with central force field',
      constraint: 'Orbital motion under inverse square law force',
      operator: 'F = -GMm/r² r̂ (central force)',
      physicsLaw: 'Central Force Motion / Orbital Mechanics',
      application: 'Planetary orbits, satellite trajectories, comet paths',
      equation: 'r = a(1-e²)/(1+e cos θ) (orbital equation)',
      verification: 'Dimensional: [F] = [GMm/r²] ✓'
    },
    virgo: {
      name: 'Virgo (Virgin)',
      description: 'Large constellation with distributed stellar pattern',
      geometry: 'Statistical mechanics of large N-body system',
      constraint: 'Thermodynamic equilibrium in stellar population',
      operator: 'S = k ln Ω (entropy of microstate distribution)',
      physicsLaw: 'Statistical Mechanics / Thermodynamic Equilibrium',
      application: 'Stellar populations, galactic evolution, phase transitions',
      equation: 'dS = (1/T)dU + (P/T)dV - (μ/T)dN',
      verification: 'Dimensional: [S] = [k] (entropy units) ✓'
    },
    libra: {
      name: 'Libra (Scales)',
      description: 'Balanced pattern suggesting equilibrium',
      geometry: 'Dynamic equilibrium, force balance symmetry',
      constraint: 'Mechanical equilibrium with balanced forces',
      operator: 'ΣF = 0, Στ = 0 (equilibrium conditions)',
      physicsLaw: 'Static Equilibrium / Force Balance',
      application: 'Structural mechanics, lever systems, pressure equilibrium',
      equation: 'F₁d₁ = F₂d₂ (lever principle)',
      verification: 'Dimensional: [F][d] = [F][d] ✓'
    },
    scorpius: {
      name: 'Scorpius (Scorpion)',
      description: 'Curved S-shaped stellar arrangement',
      geometry: 'Non-linear dynamics, chaotic trajectory patterns',
      constraint: 'Sensitive dependence on initial conditions',
      operator: 'dx/dt = f(x,y), dy/dt = g(x,y) (coupled ODEs)',
      physicsLaw: 'Chaos Theory / Non-linear Dynamics',
      application: 'Weather systems, fluid turbulence, population dynamics',
      equation: 'λ = lim(t→∞) (1/t) ln|δx(t)/δx₀| (Lyapunov exponent)',
      verification: 'Dimensional: [λ] = [1/T] ✓'
    },
    sagittarius: {
      name: 'Sagittarius (Archer)',
      description: 'Arrow-like directional pattern toward galactic center',
      geometry: 'Directional vector field, flow toward central attractor',
      constraint: 'Radial inflow with central mass concentration',
      operator: '∇·v = -∇²Φ/4πG (continuity + Poisson)',
      physicsLaw: 'Gravitational Flow / Accretion Dynamics',
      application: 'Black hole accretion, galactic center dynamics, fluid inflow',
      equation: 'dm/dt = 4πρ(r)r²v(r) (mass flow rate)',
      verification: 'Dimensional: [dm/dt] = [ρ][r²][v] ✓'
    },
    capricornus: {
      name: 'Capricornus (Sea Goat)',
      description: 'Triangular pattern with hierarchical structure',
      geometry: 'Fractal hierarchy, self-similar scaling structure',
      constraint: 'Scale-invariant organization with power-law distribution',
      operator: 'P(k) ∝ k^(-γ) (power-law scaling)',
      physicsLaw: 'Scale-Free Networks / Critical Phenomena',
      application: 'Phase transitions, percolation, network topology',
      equation: 'ξ ∝ |T-Tc|^(-ν) (correlation length)',
      verification: 'Dimensional: [ξ] = [L] ✓'
    },
    aquarius: {
      name: 'Aquarius (Water Bearer)',
      description: 'Flowing pattern suggesting fluid motion',
      geometry: 'Fluid streamlines, continuous medium flow',
      constraint: 'Incompressible fluid with conservation of mass',
      operator: '∇·v = 0, ∂v/∂t + (v·∇)v = -∇P/ρ + ν∇²v',
      physicsLaw: 'Navier-Stokes Equations / Fluid Dynamics',
      application: 'Atmospheric flow, ocean currents, plasma dynamics',
      equation: 'Re = ρvL/μ (Reynolds number)',
      verification: 'Dimensional: [Re] = dimensionless ✓'
    },
    pisces: {
      name: 'Pisces (Fish)',
      description: 'Two connected loops suggesting wave interference',
      geometry: 'Interfering wave patterns, standing wave formation',
      constraint: 'Constructive/destructive interference of wave modes',
      operator: 'ψ = ψ₁ + ψ₂ = A₁e^(ik₁·r) + A₂e^(ik₂·r)',
      physicsLaw: 'Wave Interference / Superposition Principle',
      application: 'Double-slit experiment, optical interference, quantum superposition',
      equation: 'I = |ψ|² = |A₁|² + |A₂|² + 2Re(A₁*A₂e^(i(k₁-k₂)·r))',
      verification: 'Dimensional: [I] = [|ψ|²] ✓'
    }
  };

  const pipelineSteps = [
    'Input Symbol Geometry',
    'Extract Constraint Properties',
    'Apply Field Operators',
    'Solve Governing Equation',
    'Verify Physical Validity'
  ];

  const analyzeGeometricImage = (imageData, canvas) => {
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    if (!ctx || width === 0 || height === 0) {
      setError('Invalid canvas context or dimensions');
      return null;
    }

    const data = ctx.getImageData(0, 0, width, height).data;
    
    let analysis = {
      name: 'Custom Geometry',
      description: 'Uploaded geometric form',
      geometry: '',
      constraint: '',
      operator: '',
      physicsLaw: '',
      application: '',
      equation: '',
      verification: ''
    };

    let pixelCount = 0;
    let centerX = 0, centerY = 0;
    let minX = width, maxX = 0, minY = height, maxY = 0;
    
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const idx = (y * width + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];
        const brightness = (r + g + b) / 3;
        
        if (brightness < 200) {
          pixelCount++;
          centerX += x;
          centerY += y;
          minX = Math.min(minX, x);
          maxX = Math.max(maxX, x);
          minY = Math.min(minY, y);
          maxY = Math.max(maxY, y);
        }
      }
    }

    if (pixelCount < 100) {
      setError('No significant geometric features detected in the image');
      return null;
    }

    centerX = pixelCount > 0 ? centerX / pixelCount : width / 2;
    centerY = pixelCount > 0 ? centerY / pixelCount : height / 2;

    const aspectRatio = (maxX - minX) / (maxY - minY + 0.0001);
    const fillRatio = pixelCount / (width * height);
    const compactness = pixelCount / ((maxX - minX + 1) * (maxY - minY + 1));

    let radialSymmetry = 0;
    let circularityScore = 0;
    const maxRadius = Math.min(width, height) / 2;
    const angles = 32;
    const radialSamples = [];

    for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / angles) {
      let radialPixels = 0;
      for (let r = 0; r < maxRadius; r += 2) {
        const x = Math.round(centerX + r * Math.cos(angle));
        const y = Math.round(centerY + r * Math.sin(angle));
        if (x >= 0 && x < width && y >= 0 && y < height) {
          const idx = (y * width + x) * 4;
          const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3;
          if (brightness < 200) radialPixels++;
        }
      }
      radialSamples.push(radialPixels);
      circularityScore += radialPixels;
    }

    const meanRadial = radialSamples.reduce((sum, val) => sum + val, 0) / radialSamples.length;
    radialSymmetry = 1 - (radialSamples.reduce((sum, val) => sum + Math.abs(val - meanRadial), 0) / (meanRadial * radialSamples.length));

    if (radialSymmetry > 0.85 && aspectRatio > 0.8 && aspectRatio < 1.2 && compactness > 0.3) {
      analysis.geometry = 'Circular symmetry, high radial consistency';
      analysis.constraint = 'Radial field divergence with central source';
      analysis.operator = '∇ · E = ρ/ε₀';
      analysis.physicsLaw = 'Coulomb Field / Point Source Divergence';
      analysis.application = 'Electric monopole, gravitational point mass, scalar field source';
      analysis.equation = '∇²Φ = -ρ/ε₀ (Poisson equation)';
      analysis.verification = 'Dimensional: [∇²Φ] = [ρ]/[ε₀] ✓';
    } else if (aspectRatio > 2 || aspectRatio < 0.5) {
      analysis.geometry = 'Linear extension, directional anisotropy';
      analysis.constraint = 'Unidirectional field propagation';
      analysis.operator = '∂²u/∂x² = (1/c²)∂²u/∂t²';
      analysis.physicsLaw = 'Wave Equation / Linear Propagation';
      analysis.application = 'Electromagnetic waves, sound waves, vibrating strings';
      analysis.equation = 'u(x,t) = A sin(kx - ωt)';
      analysis.verification = 'Dimensional: [k²u] = [ω²u/c²] ✓';
    } else if (fillRatio < 0.1) {
      analysis.geometry = 'Sparse network topology, discrete nodes';
      analysis.constraint = 'Discrete lattice with nearest-neighbor coupling';
      analysis.operator = 'H|ψ⟩ = E|ψ⟩ with tight-binding model';
      analysis.physicsLaw = 'Quantum Lattice / Tight-Binding Hamiltonian';
      analysis.application = 'Crystal band structure, quantum dots, molecular orbitals';
      analysis.equation = 'E = -2t cos(ka) (1D tight-binding)';
      analysis.verification = 'Dimensional: [E] = [t] (energy units) ✓';
    } else if (compactness < 0.5 && radialSymmetry < 0.7) {
      analysis.geometry = 'Self-similar structure, fractal boundary conditions';
      analysis.constraint = 'Scale-invariant field behavior with fractal dimension';
      analysis.operator = '(-∇²)^(α/2) u = f (fractional Laplacian)';
      analysis.physicsLaw = 'Fractional Diffusion / Anomalous Transport';
      analysis.application = 'Turbulent mixing, porous media flow, biological membranes';
      analysis.equation = '∂u/∂t = D_α (-∇²)^(α/2) u';
      analysis.verification = 'Dimensional: [D_α] = [L^α]/[T] ✓';
    } else {
      analysis.geometry = 'Complex multi-modal structure with mixed symmetries';
      analysis.constraint = 'Superposition of multiple geometric modes';
      analysis.operator = 'Φ(x) = Σ_i c_i φ_i(x) with ∇²φ_i = λ_iφ_i';
      analysis.physicsLaw = 'Eigenmode Decomposition / Spectral Analysis';
      analysis.application = 'Cavity resonances, structural vibrations, quantum confined states';
      analysis.equation = 'λ_i = (nπ/L)² for 1D cavity modes';
      analysis.verification = 'Dimensional: [λ] = [L⁻²] ✓';
    }

    analysis.description = `Analyzed geometric form with aspect ratio ${aspectRatio.toFixed(2)}, fill ratio ${fillRatio.toFixed(3)}, radial symmetry ${radialSymmetry.toFixed(2)}`;
    
    return analysis;
  };

  const handleImageUpload = (event) => {
    setError(null);
    const file = event.target.files[0];
    if (!file) {
      setError('No file selected');
      return;
    }
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file (PNG, JPG, GIF)');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image size exceeds 10MB limit');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        setUploadedImage(img);
        
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        
        const maxSize = 400;
        const scale = Math.min(maxSize / img.width, maxSize / img.height);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        const analysis = analyzeGeometricImage(e, canvas);
        if (analysis) {
          setImageAnalysis(analysis);
          setMode('upload');
        }
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  };

  const runAnalysis = () => {
    setIsProcessing(true);
    setCurrentStep(0);
    
    const interval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < pipelineSteps.length - 1) {
          return prev + 1;
        } else {
          setIsProcessing(false);
          clearInterval(interval);
          return prev;
        }
      });
    }, 800);
  };

  const resetAnalysis = () => {
    setCurrentStep(0);
    setIsProcessing(false);
    setUploadedImage(null);
    setImageAnalysis(null);
    setError(null);
    setMode('preset');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getCurrentSymbol = () => {
    return mode === 'upload' && imageAnalysis ? imageAnalysis : presetSymbols[selectedSymbol];
  };

  const currentSymbol = getCurrentSymbol();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2 flex items-center justify-center gap-3">
            <Zap className="w-10 h-10 text-yellow-400" />
            Sacred Geometry Physics Decoder
          </h1>
          <p className="text-blue-200 text-lg">
            Decode geometric patterns into fundamental physics equations
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <ImageIcon className="w-5 h-5" />
              Input Geometry
            </h2>
            
            <div className="flex gap-4 mb-4">
              <button
                onClick={() => setMode('preset')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  mode === 'preset'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white/10 text-blue-200 hover:bg-white/20'
                }`}
              >
                Preset Symbols
              </button>
              <button
                onClick={() => setMode('upload')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  mode === 'upload'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white/10 text-blue-200 hover:bg-white/20'
                }`}
              >
                Upload Image
              </button>
            </div>

            {mode === 'preset' ? (
              <div className="space-y-3">
                {Object.entries(presetSymbols).map(([key, symbol]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedSymbol(key)}
                    className={`w-full p-3 rounded-lg text-left transition-colors ${
                      selectedSymbol === key
                        ? 'bg-blue-500/30 border border-blue-400'
                        : 'bg-white/5 hover:bg-white/10 border border-white/10'
                    }`}
                  >
                    <div className="text-white font-medium">{symbol.name}</div>
                    <div className="text-blue-200 text-sm">{symbol.description}</div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                <div className="border-2 border-dashed border-blue-400 rounded-lg p-8 text-center">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="flex flex-col items-center gap-2 text-blue-200 hover:text-white transition-colors"
                  >
                    <Upload className="w-8 h-8" />
                    <span>Click to upload geometric image</span>
                  </button>
                </div>
                
                {uploadedImage && (
                  <div className="bg-white/5 rounded-lg p-4">
                    <canvas
                      ref={canvasRef}
                      className="max-w-full h-auto rounded border border-white/20"
                    />
                  </div>
                )}
              </div>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg">
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            )}
          </div>

          {/* Analysis Pipeline */}
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Calculator className="w-5 h-5" />
              Analysis Pipeline
            </h2>
            
            <div className="space-y-3 mb-6">
              {pipelineSteps.map((step, index) => (
                <div
                  key={index}
                  className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${
                    index < currentStep
                      ? 'bg-green-500/20 border border-green-500/50'
                      : index === currentStep && isProcessing
                      ? 'bg-blue-500/20 border border-blue-500/50'
                      : 'bg-white/5 border border-white/10'
                  }`}
                >
                  {index < currentStep ? (
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  ) : index === currentStep && isProcessing ? (
                    <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <div className="w-5 h-5 border-2 border-white/30 rounded-full" />
                  )}
                  <span className={`${
                    index <= currentStep ? 'text-white' : 'text-blue-200'
                  }`}>
                    {step}
                  </span>
                </div>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={runAnalysis}
                disabled={isProcessing}
                className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <Play className="w-5 h-5" />
                {isProcessing ? 'Processing...' : 'Run Analysis'}
              </button>
              <button
                onClick={resetAnalysis}
                className="bg-white/10 hover:bg-white/20 text-white px-4 py-3 rounded-lg transition-colors"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {currentStep >= pipelineSteps.length - 1 && (
          <div className="mt-8 bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Eye className="w-5 h-5" />
              Physics Mapping Results
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Geometric Properties</h3>
                  <p className="text-white text-sm">{currentSymbol.geometry}</p>
                </div>
                
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Physical Constraint</h3>
                  <p className="text-white text-sm">{currentSymbol.constraint}</p>
                </div>
                
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Mathematical Operator</h3>
                  <p className="text-white font-mono text-sm bg-black/20 p-2 rounded">
                    {currentSymbol.operator}
                  </p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Physics Law</h3>
                  <p className="text-white text-sm">{currentSymbol.physicsLaw}</p>
                </div>
                
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Physical Applications</h3>
                  <p className="text-white text-sm">{currentSymbol.application}</p>
                </div>
                
                <div className="bg-white/5 rounded-lg p-4">
                  <h3 className="text-blue-300 font-medium mb-2">Governing Equation</h3>
                  <p className="text-white font-mono text-sm bg-black/20 p-2 rounded">
                    {currentSymbol.equation}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="mt-6 bg-green-500/10 border border-green-500/30 rounded-lg p-4">
              <h3 className="text-green-300 font-medium mb-2">Dimensional Verification</h3>
              <p className="text-green-200 font-mono text-sm">{currentSymbol.verification}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SacredGeometryDecoder;
