"""
Example usage of Cutaneous Laser Speckle Contrast Imaging (LSCI) Skill.
Demonstrates static low-flow tissue vs normal capillary perfusion vs reactive hyperemia.
"""

import json
from client import LaserSpeckleContrastClient


def main():
    print("=== Testing Cutaneous Laser Speckle Contrast Imaging (LSCI) Skill ===")
    client = LaserSpeckleContrastClient(camera_exposure_time_s=0.005)

    # 1. Static tissue / complete arterial occlusion (high variance, speckles sharp -> K ~ 0.70)
    static_pixels = [20.0, 180.0, 30.0, 190.0, 25.0, 175.0, 35.0, 185.0, 22.0, 195.0, 28.0, 182.0]
    res_static = client.analyze_speckle_region(static_pixels)
    print("\n[Case 1: Static Tissue / Occlusion]")
    print(json.dumps(res_static, indent=2))

    # 2. Normal resting microvascular perfusion (blurred speckle -> K ~ 0.25)
    normal_pixels = [100.0, 125.0, 95.0, 115.0, 105.0, 120.0, 98.0, 110.0, 102.0, 118.0, 108.0, 112.0]
    res_normal = client.analyze_speckle_region(normal_pixels)
    print("\n[Case 2: Normal Cutaneous Capillary Perfusion]")
    print(json.dumps(res_normal, indent=2))

    # 3. Post-occlusive reactive hyperemia (maximal blurring -> K ~ 0.10)
    hyperemic_pixels = [110.0, 115.0, 108.0, 112.0, 111.0, 114.0, 109.0, 113.0, 110.0, 112.0, 111.0, 113.0]
    res_hyperemic = client.analyze_speckle_region(hyperemic_pixels)
    print("\n[Case 3: Reactive Hyperemia / Maximal Blurring]")
    print(json.dumps(res_hyperemic, indent=2))

    # Assertions
    assert res_static["speckle_contrast_k"] > res_normal["speckle_contrast_k"]
    assert res_normal["speckle_contrast_k"] > res_hyperemic["speckle_contrast_k"]
    assert res_hyperemic["laser_speckle_perfusion_units_lspu"] > res_normal["laser_speckle_perfusion_units_lspu"]
    print("\n[SUCCESS] Laser Speckle Contrast Imaging tests passed!")


if __name__ == "__main__":
    main()
