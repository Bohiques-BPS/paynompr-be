from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database.config import session
from models.periods import Period
from controllers.period import create_weekly_periods, create_biweekly_periods, create_monthly_periods


def initialize_periods():
    try:
        # Create periods for the current year and the previous year
        current_year = date.today().year
        previous_year = current_year - 1

        create_weekly_periods(previous_year)
        create_weekly_periods(current_year)
        create_biweekly_periods(previous_year)
        create_biweekly_periods(current_year)
        create_monthly_periods(previous_year)
        create_monthly_periods(current_year)

        session.commit()
        print("Periods initialized successfully")
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while initializing periods: {e}",
        )
    finally:
        session.close()
