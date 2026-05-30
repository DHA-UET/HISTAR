const TOTAL_MAPS = 10;
let unlockedMaps = new Set();

const loadProgress = () => {
    const saved = localStorage.getItem('ar_museum_progress');
    if (saved) unlockedMaps = new Set(JSON.parse(saved));
};

const saveProgress = () => {
    localStorage.setItem('ar_museum_progress', JSON.stringify([...unlockedMaps]));
};

const updateHUD = () => {
    document.getElementById('mission-counter').innerText = `[ ${unlockedMaps.size} / ${TOTAL_MAPS} ]`;
    if (unlockedMaps.size >= TOTAL_MAPS) {
        setTimeout(() => {
            document.getElementById('completion-screen').style.display = 'flex';
        }, 1500);
    }
};

const showToast = (message) => {
    const toast = document.getElementById('toast-msg');
    toast.innerText = message;
    toast.classList.add('show-toast');
    setTimeout(() => {
        toast.classList.remove('show-toast');
    }, 4000);
};

document.addEventListener("DOMContentLoaded", function () {
    loadProgress();
    const startScreen = document.getElementById("start-screen");
    const uiLayer = document.getElementById("ui-layer");
    const startBtn = document.getElementById("start-btn");
    const clearDataBtn = document.getElementById("clear-data-btn");
    const resetBtn = document.getElementById("reset-btn");

    updateHUD();

    startBtn.addEventListener("click", function () {
        const videos = document.querySelectorAll('video');
        videos.forEach(vid => {
            vid.play().then(() => {
                vid.pause();
            }).catch(e => console.log(e));
        });
        startScreen.style.display = "none";
        uiLayer.style.display = "block";
    });

    clearDataBtn.addEventListener("click", function () {
        if (confirm("CẢNH BÁO: Bạn có chắc chắn muốn xóa toàn bộ dữ liệu đã thu thập và chơi lại từ đầu?")) {
            localStorage.removeItem('ar_museum_progress');
            unlockedMaps.clear();
            updateHUD();
            alert("Đã xóa dữ liệu thành công! Bạn có thể bắt đầu lại.");
        }
    });

    resetBtn.addEventListener("click", function() {
        localStorage.removeItem('ar_museum_progress');
        location.reload();
    });
});

AFRAME.registerComponent('map-tracker', {
    schema: {
        targetId: { type: 'number' },
        targetName: { type: 'string', default: 'Dữ liệu không xác định' }
    },
    init: function () {
        this.el.addEventListener('targetFound', () => {
            const id = this.data.targetId;
            const name = this.data.targetName;

            if (!unlockedMaps.has(id)) {
                unlockedMaps.add(id);
                saveProgress();
                updateHUD();
                showToast(`ĐÃ TÌM THẤY CHIẾN DỊCH MỚI:\n${name}`);
            }
        });
    }
});

AFRAME.registerComponent('chromakey-video', {
    schema: {
        src: { type: 'selector' },
        color: { type: 'color', default: '#00ff00' },
        threshold: { type: 'number', default: 0.4 }
    },
    init: function () {
        this.videoEl = this.data.src;
        if (!this.videoEl) return;

        this.texture = new THREE.VideoTexture(this.videoEl);
        this.texture.minFilter = THREE.LinearFilter;
        this.texture.magFilter = THREE.LinearFilter;
        this.texture.format = THREE.RGBAFormat;
        const keyColor = new THREE.Color(this.data.color);

        this.material = new THREE.ShaderMaterial({
            uniforms: {
                color: { value: keyColor },
                tex: { value: this.texture },
                threshold: { value: this.data.threshold }
            },
            vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
            fragmentShader: `uniform vec3 color; uniform sampler2D tex; uniform float threshold; varying vec2 vUv;
                void main() {
                    vec4 tColor = texture2D(tex, vUv);
                    float diff = length(tColor.rgb - color);
                    if (diff < threshold) { discard; } else { gl_FragColor = tColor; }
                }`,
            transparent: true,
            side: THREE.DoubleSide
        });

        const applyMat = () => {
            const mesh = this.el.getObject3D('mesh');
            if (mesh) mesh.material = this.material;
        };
        applyMat();
        this.el.addEventListener('object3dset', applyMat);
    },
    tick: function () {
        if (this.texture && this.videoEl.readyState >= this.videoEl.HAVE_CURRENT_DATA) {
            this.texture.needsUpdate = true;
        }
    }
});

AFRAME.registerComponent('video-handler', {
    schema: { video: { type: 'string' } },
    init: function () {
        const video = document.querySelector(this.data.video);
        this.el.addEventListener('targetFound', () => {
            if (video) video.play();
        });
        this.el.addEventListener('targetLost', () => {
            if (video) video.pause();
        });
    }
});
