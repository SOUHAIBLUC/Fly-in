from __future__ import annotations
 
import re
from dataclasses import dataclass, field
from typing import Optional

VALID_ZONE_TYPE = {"normal", "blocked", "restricted", "priority"}

@dataclass
class zone:
	"single zone (node) in the drone network."

	name :  str
	x : int
	y : int
	zone_type : str = "normal"
	zone_clore : Optional[str] = "None"
	max_dron : int = 1
	is_end : bool = False
	is_start : bool = False

