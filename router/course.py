from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import crud, schemas
from fastapi import APIRouter
import validation


router=APIRouter()


@router.post("/createcourse/", response_model=schemas.course)
def create_course(course: schemas.course, db: Session = Depends(get_db)):
    validation.checkcourse(value=course)
    db_course = crud.get_course(db=db,course_id=course.CID) 
    if db_course:
        raise HTTPException(status_code=400, detail="درس وجود دارد")
    return crud.create_course(db=db, course=course)
 

@router.get("/getcourse/{course_id}",response_model=schemas.course) 
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="درس یافت نشد")
    return db_course


@router.put("/updatecourse/{id}")
def update_course(course: schemas.course,id:int ,db: Session = Depends(get_db)):
    db_course=crud.get_course(db=db,course_id=id )
    if db_course is None:
        raise HTTPException(status_code=400,detail="درس یافت نشد")
    if course.CID !=id :
        db_course=crud.get_course(db=db,course_id=course.CID )
        if db_course :
            raise HTTPException(status_code=400,detail="کد درس وارد شده تکراری است")       
    validation.checkcourse(course)
    crud.update_course(db=db,data=course,id=id)
    return "به روز رسانی درس موفقیت امیز بود"


@router.delete("/deletecourse/{id}")
def delete_course(id:int,db:Session=Depends(get_db)):
    db_course=crud.get_course(db=db,course_id=id)
    if db_course is None:
        raise HTTPException(status_code=400,detail="درس یافت نشد")
    crud.delete_course(db=db,id=id)
    return "درس حذف شد"
