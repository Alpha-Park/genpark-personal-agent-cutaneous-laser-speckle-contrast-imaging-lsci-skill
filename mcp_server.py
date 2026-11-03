"""
MCP Server for Cutaneous Laser Speckle Contrast Imaging (LSCI) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import LaserSpeckleContrastClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cutaneous-laser-speckle-contrast-imaging-lsci-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_speckle_region",
                        "description": "Calculate speckle contrast K, Blood Flow Index (BFI), and Laser Speckle Perfusion Units (LSPU) to evaluate microvascular flow.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "pixel_intensities": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Array of pixel intensities in a local kernel (min 9 samples)."
                                },
                                "camera_exposure_time_s": {"type": "number", "description": "Exposure duration in seconds (default: 0.005)."},
                                "dark_noise_offset": {"type": "number", "description": "Background dark noise count (default: 0.0)."}
                            },
                            "required": ["pixel_intensities"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_speckle_region":
            exp_time = float(args.get("camera_exposure_time_s", 0.005))
            dark_offset = float(args.get("dark_noise_offset", 0.0))
            pixels = args.get("pixel_intensities", [])
            client = LaserSpeckleContrastClient(camera_exposure_time_s=exp_time)
            try:
                res = client.analyze_speckle_region(
                    pixel_intensities=[float(p) for p in pixels],
                    dark_noise_offset=dark_offset
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
