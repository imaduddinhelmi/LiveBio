"""
Color utility functions for adaptive text colors based on background brightness
"""

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_luminance(rgb):
    """
    Calculate relative luminance of a color
    Uses the formula from WCAG 2.0
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    # Apply gamma correction
    def adjust(c):
        if c <= 0.03928:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = adjust(r), adjust(g), adjust(b)
    
    # Calculate luminance
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_color(bg_color, light_color="#E8E8E8", dark_color="#2B2B2B"):
    """
    Get contrasting text color based on background brightness
    
    Args:
        bg_color: Background color in hex format
        light_color: Color to use for light text (on dark backgrounds)
        dark_color: Color to use for dark text (on light backgrounds)
    
    Returns:
        Appropriate text color (light or dark)
    """
    try:
        rgb = hex_to_rgb(bg_color)
        luminance = calculate_luminance(rgb)
        
        # If background is bright (luminance > 0.5), use dark text
        # If background is dark (luminance <= 0.5), use light text
        return dark_color if luminance > 0.5 else light_color
    except:
        # Default to light text if calculation fails
        return light_color

def get_soft_color(base_color, is_dark_mode=True):
    """
    Get softer version of a color for better visual comfort
    
    Args:
        base_color: Base color in hex format
        is_dark_mode: Whether in dark mode
    
    Returns:
        Softer version of the color
    """
    try:
        r, g, b = hex_to_rgb(base_color)
        
        if is_dark_mode:
            # In dark mode, slightly brighten colors
            factor = 1.2
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
        else:
            # In light mode, slightly darken colors
            factor = 0.85
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return base_color

def get_adaptive_text_color(is_dark_mode=True):
    """
    Get adaptive text color based on theme mode
    
    Args:
        is_dark_mode: Whether application is in dark mode
    
    Returns:
        Appropriate text color
    """
    if is_dark_mode:
        return "#E8E8E8"  # Soft light gray for dark backgrounds
    else:
        return "#2B2B2B"  # Soft dark gray for light backgrounds

def get_adaptive_gray_color(is_dark_mode=True):
    """
    Get adaptive gray color for secondary text
    
    Args:
        is_dark_mode: Whether application is in dark mode
    
    Returns:
        Appropriate gray color
    """
    if is_dark_mode:
        return "#A0A0A0"  # Medium gray for dark backgrounds
    else:
        return "#666666"  # Darker gray for light backgrounds

def get_adaptive_success_color(is_dark_mode=True):
    """Get adaptive green color for success messages"""
    if is_dark_mode:
        return "#5CDB5C"  # Brighter green for dark backgrounds
    else:
        return "#2E7D32"  # Darker green for light backgrounds

def get_adaptive_error_color(is_dark_mode=True):
    """Get adaptive red color for error messages"""
    if is_dark_mode:
        return "#FF6B6B"  # Softer red for dark backgrounds
    else:
        return "#C62828"  # Darker red for light backgrounds

def get_adaptive_warning_color(is_dark_mode=True):
    """Get adaptive orange color for warning messages"""
    if is_dark_mode:
        return "#FFB74D"  # Brighter orange for dark backgrounds
    else:
        return "#F57C00"  # Darker orange for light backgrounds

def get_adaptive_info_color(is_dark_mode=True):
    """Get adaptive blue color for info messages"""
    if is_dark_mode:
        return "#64B5F6"  # Brighter blue for dark backgrounds
    else:
        return "#1976D2"  # Darker blue for light backgrounds
