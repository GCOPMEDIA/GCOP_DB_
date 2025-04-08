import requests

url = "https://gcop-db.onrender.com/check-id"
data = {"id": "GCOP-0005"}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())  # Print JSON response
# from fpdf import FPDF
#
#
# def create_id_template():
#     # Create PDF object
#     pdf = FPDF(orientation='P', unit='mm', format=(85, 54))  # ID card size (typical dimensions)
#
#     # Add a page
#     pdf.add_page()
#
#     # Set font and colors
#     pdf.set_font("Arial", "B", 16)
#     pdf.set_text_color(0, 0, 0)  # Black text
#
#     # Add church name at the top
#     pdf.cell(0, 10, "GOD'S CHURCH OF PEACE INTERNATIONAL", ln=1, align='C')
#
#     # Add "MERCY TEMPLE" below
#     pdf.set_font("Arial", "B", 14)
#     pdf.cell(0, 8, "MERCY TEMPLE", ln=1, align='C')
#
#     # Add some space
#     pdf.ln(5)
#
#     # Add "Surname" label
#     pdf.set_font("Arial", "B", 10)
#     pdf.cell(40, 6, "Surname", ln=0)
#
#     # Add line for surname
#     pdf.set_font("Arial", "", 10)
#     pdf.cell(0, 6, "_________________________", ln=1)
#
#     # Add "SAMUEL NYARKO" (example name)
#     pdf.set_font("Arial", "B", 12)
#     pdf.cell(0, 8, "SAMUEL NYARKO", ln=1, align='C')
#
#     # Add "Personal ID Number" label
#     pdf.set_font("Arial", "B", 10)
#     pdf.cell(60, 6, "Personal ID Number", ln=0)
#
#     # Add line for ID number
#     pdf.set_font("Arial", "", 10)
#     pdf.cell(0, 6, "_______________", ln=1)
#
#     # Add footer text
#     pdf.ln(5)
#     pdf.set_font("Arial", "I", 8)
#     pdf.cell(0, 5, "This is the property of", ln=1, align='C')
#     pdf.set_font("Arial", "B", 9)
#     pdf.cell(0, 5, "GOD'S CHURCH OF PEACE INTERNATIONAL", ln=1, align='C')
#
#     # Add contact information
#     pdf.set_font("Arial", "", 8)
#     pdf.cell(0, 5, "If found, please contact", ln=1, align='C')
#     pdf.set_font("Arial", "", 9)
#     pdf.cell(0, 5, "+233204636990  +233240975288", ln=1, align='C')
#     pdf.set_font("Arial", "", 9)
#     pdf.cell(0, 5, "gcopmedia@gmail.com", ln=1, align='C')
#
#     # Output the PDF
#     pdf.output("church_id_template.pdf")
#
#
# create_id_template()
# from aspose.psd import Image
# from aspose.psd.fileformats.psd.layers import TextLayer
#
# # Load TIFF file
# tiff = Image.load("Nana Nyako.tif")
#
# # Loop through layers to find text
# for layer in tiff.layers:
#     if isinstance(layer, TextLayer):
#         layer.text = "Updated Text Here"  # Modify text
#         layer.update_text()
#
# # Save updated TIFF
# tiff.save("updated.tif")

#
# from aspose.psd import Image, ResizeType, Color, Rectangle
# from aspose.psd.fileformats.png import PngColorType
# from aspose.psd.fileformats.psd import PsdImage
# from aspose.psd.imageloadoptions import PsdLoadOptions
# from aspose.psd.imageoptions import PngOptions
# from aspose.pycore import cast
#
#
#
# source = "Nana Nyako copy.psd"
# output_original = "original_layer_manipulation.png"
# output_updated = "updated_layer_manipulation.png"
# pngOpt = PngOptions()
# pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
#
# psdLoadOpt = PsdLoadOptions()
# psdLoadOpt.load_effects_resource = True
# psdLoadOpt.allow_warp_repaint = True
#
# with Image.load(source, psdLoadOpt) as image:
#     psd_image = cast(PsdImage, image)
#     psd_image.save(output_original, pngOpt)
#
#     # Resizing
#     psd_image.layers[2].resize(25, 25, ResizeType.HIGH_QUALITY_RESAMPLE)
#
#     # Rotating
#     psd_image.layers[5].rotate(45, True, Color.yellow)
#
#     # Simple Filters
#     psd_image.layers[3].adjust_contrast(3)
#
#     # Cropping
#     psd_image.layers[10].crop(Rectangle(10, 10, 20, 20))
#     # Aspose.PSD supports much more specific layer manipulation, please check https://reference.aspose.com/psd/python-net/
#
#     psd_image.save(output_updated, pngOpt)
#     print(output_updated)

#
# from aspose.psd import Image
# from aspose.psd.fileformats.psd import PsdImage
# from aspose.psd.fileformats.psd.layers import TextLayer
# from aspose.psd.imageloadoptions import PsdLoadOptions
# from aspose.pycore import cast
#
# source = "Nana Nyako copy.psd"
#
# psdLoadOpt = PsdLoadOptions()
# psdLoadOpt.load_effects_resource = True
# psdLoadOpt.allow_warp_repaint = True
#
# with Image.load(source, psdLoadOpt) as image:
#     psd_image = cast(PsdImage, image)
#
#     for layer in psd_image.layers:
#         if isinstance(layer, TextLayer):  # Ensure it's a TextLayer
#             text_layer = cast(TextLayer, layer)
#             print(f"Layer: {text_layer.name}, Text: {text_layer.text_data.contents}")

# from datetime import datetime
#
# print(datetime.today())

