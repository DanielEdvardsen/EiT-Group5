'use client';
import {useEffect, useRef} from "react";
import * as THREE from 'three';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
const brainModelPath = '/brain.obj';

export default function Brain() {
    const canvasRef = useRef(null);
    useEffect(() => {
        // initialize renderer, scene and camera
        const canvas = canvasRef.current;
        const renderer = new THREE.WebGLRenderer({canvas, antialias: true});

        renderer.setClearColor(0xFFFFFF, 1);
        renderer.setSize(750, 500);
        renderer.setPixelRatio(window.devicePixelRatio);

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.setZ(5);

        // Lightning
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(0, 10, 0);
        directionalLight.target.position.set(-5, 0, 0);
        scene.add(directionalLight);
        scene.add(directionalLight.target);

        // Orbit controls
        const controls = new OrbitControls(camera, renderer.domElement);

        // Load the model
        const loader = new OBJLoader();
        loader.load(brainModelPath, (object: THREE.Object3D<THREE.Object3DEventMap>) => {
            scene.add(object);
        }, undefined, (error) => {
            console.error('An error happened', error);
        })

        const animate = () => {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };

        animate();
    }, []);

    return <canvas ref={canvasRef} id="bg"></canvas>;
}