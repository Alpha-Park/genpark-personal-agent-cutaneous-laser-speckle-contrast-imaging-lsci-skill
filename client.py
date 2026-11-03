"""
Cutaneous Laser Speckle Contrast Imaging (LSCI) Microvascular Perfusion Client.
Zero-mock pure Python standard library implementation.
Calculates speckle contrast K = sigma / mean(I), Blood Flow Index (BFI),
and Laser Speckle Perfusion Units (LSPU) to evaluate cutaneous microcirculation.
"""

import math
from typing import Dict, Any, List, Optional


class LaserSpeckleContrastClient:
    """
    Computes Laser Speckle Contrast Imaging (LSCI) metrics:
    - Speckle Contrast K = sigma_I / mean(I)
    - Blood Flow Index (BFI) = 1 / (2 * T * K^2)
    - Perfusion Units (LSPU)
    - Spatial Perfusion Heterogeneity Coefficient (CV_flux)
    """

    def __init__(self, camera_exposure_time_s: float = 0.005):
        if camera_exposure_time_s <= 0:
            raise ValueError("Exposure time must be strictly positive.")
        self.exposure_time_s = camera_exposure_time_s

    def analyze_speckle_region(
        self,
        pixel_intensities: List[float],
        dark_noise_offset: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates speckle contrast and perfusion index from an array of pixel intensities (0 - 255 or arbitrary counts).
        pixel_intensities: Raw intensity values in a local spatial kernel (e.g., 5x5 or 7x7 window, min 9 pixels).
        dark_noise_offset: Sensor dark current background subtraction.
        """
        if not pixel_intensities or len(pixel_intensities) < 9:
            raise ValueError("Laser speckle analysis requires at least 9 pixel intensity values.")

        adjusted = [max(0.1, x - dark_noise_offset) for x in pixel_intensities]
        n = len(adjusted)

        mean_intensity = sum(adjusted) / n
        if mean_intensity <= 0:
            raise ValueError("Mean intensity must be positive.")

        variance = sum((x - mean_intensity) ** 2 for x in adjusted) / (n - 1)
        sigma = math.sqrt(variance)

        # Speckle Contrast: K = sigma / mean
        # Range is theoretically 0 (complete blurring / very high flow) to 1.0 (static speckle / zero flow)
        speckle_contrast_k = min(1.0, max(0.01, sigma / mean_intensity))

        # Blood Flow Index (BFI):
        # BFI ~ 1 / (2 * T * K^2)
        # In practical laser speckle systems, LSPU = 1000 * (1 / (K^2) - 1) or simplified BFI scaling
        bfi = 1.0 / (2.0 * self.exposure_time_s * (speckle_contrast_k ** 2))
        lspu = bfi * 0.10  # Scaled to standard Laser Speckle Perfusion Units (0 - 2000 LSPU)

        # Spatial microvascular flow state:
        # Static tissue / occlusion: K > 0.65, LSPU < 150
        # Normal resting dermal capillary flow: K ~ 0.20 - 0.45, LSPU 300 - 800
        # Hyperemic / vasodilatory surge: K < 0.15, LSPU > 1200
        if speckle_contrast_k > 0.60:
            perfusion_state = "Severe Ischemia / Occlusion / Static Microvasculature"
            microvascular_status = "Minimal erythrocyte transit; high speckle contrast indicates immobile scatterers."
            flux_reserve = "Depleted"
        elif speckle_contrast_k > 0.35:
            perfusion_state = "Low-Normal Resting Dermal Perfusion"
            microvascular_status = "Subdued basal capillary flux; physiological in cool ambient conditions."
            flux_reserve = "Normal Resting"
        elif speckle_contrast_k > 0.18:
            perfusion_state = "Optimal Dermal Capillary Perfusion"
            microvascular_status = "Well-perfused papillary loops with rapid Brownian and convective red blood cell motion."
            flux_reserve = "Optimal"
        else:
            perfusion_state = "Hyperdynamic Reactive Hyperemia / Vasodilatation"
            microvascular_status = "Pronounced speckle blurring reflecting maximal capillary and arteriolar flow velocity."
            flux_reserve = "Maximal Active"

        return {
            "status": "success",
            "pixel_sample_count": n,
            "mean_intensity": round(mean_intensity, 2),
            "intensity_std_dev": round(sigma, 2),
            "speckle_contrast_k": round(speckle_contrast_k, 4),
            "blood_flow_index_bfi": round(bfi, 1),
            "laser_speckle_perfusion_units_lspu": round(lspu, 1),
            "exposure_time_ms": round(self.exposure_time_s * 1000.0, 2),
            "evaluation": {
                "perfusion_state": perfusion_state,
                "microvascular_status": microvascular_status,
                "flux_reserve": flux_reserve
            }
        }
