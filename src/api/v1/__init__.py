from fastapi import APIRouter, Depends, HTTPException, Path, status

from services import SecurityService


router = APIRouter()