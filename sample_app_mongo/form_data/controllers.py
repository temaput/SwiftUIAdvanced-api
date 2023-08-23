from fastapi import APIRouter, Request

from .models import PlainForm, PlainFormWithFile
from starlette.datastructures import UploadFile

router = APIRouter()

print(PlainForm.schema())


@router.post("/flat-form-raw/",
             openapi_extra={
                 "requestBody": {
                     "content": {
                         "multipart/form-data": {
                             "schema": PlainFormWithFile.schema()
                         }
                     },
                     "required": True,
                 },
             })
async def create_item(request: Request):
    async with request.form() as formdata:
        print(formdata)
        for field in formdata.keys():
            value = formdata.get(field)
            if isinstance(value, UploadFile):
                print("Saving file: %s (%s)" %
                      (value.filename, value.content_type))
                with open('media/' + (value.filename or 'unknown'), 'wb') as f:
                    f.write(await value.read())

    return "ok"