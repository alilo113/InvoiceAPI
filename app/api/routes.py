from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict
from app.services.invoice_logic import invoice_input_validation, calculate_invoice_totals
from app.services.pdf_generator import generate_invoice_pdf

invoice_router = APIRouter()

@invoice_router.post("/")
async def generate_invoice(invoice_data: Dict):

    # Validate
    valid, msg = invoice_input_validation(invoice_data)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    # Calculate
    result = calculate_invoice_totals(invoice_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Generate PDF
    try:
        pdf_buffer = generate_invoice_pdf(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    # Return PDF
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=invoice_{result['invoice_number']}.pdf"
        }
    )