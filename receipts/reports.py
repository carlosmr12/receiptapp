import pandas as pd
import plotly.express as px
from django.db.models import Sum
from datetime import date, timedelta

def generate_expenses_by_category_pie(receipts_queryset):
    """Generates a pie chart of expenses by category."""
    data = receipts_queryset.values('category__name').annotate(total=Sum('total_amount'))
    df = pd.DataFrame(list(data))

    if df.empty:
        return "<p>No data to display for expenses by category.</p>"

    fig = px.pie(df, values='total', names='category__name', title='Expenses by Category')
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_spending_over_time_bar(receipts_queryset, period='all_time'):
    """Generates a bar chart of spending over time (daily, weekly, or monthly)."""
    df = pd.DataFrame(list(receipts_queryset.filter(date_of_purchase__isnull=False).values('date_of_purchase', 'total_amount', 'user__username')))

    if df.empty:
        return "<p>No data to display for spending over time.</p>"

    df['date_of_purchase'] = pd.to_datetime(df['date_of_purchase'])

    # Determine grouping frequency and x-axis label
    if period == 'last_7_days':
        df['period_group'] = df['date_of_purchase'].dt.date # Group by day
        x_axis_title = 'Day'
        # Generate full date range for the last 7 days
        today = date.today()
        start_date = today - timedelta(days=6)
        full_range = pd.date_range(start=start_date, end=today, freq='D').date
    elif period == 'this_month':
        df['period_group'] = df['date_of_purchase'].dt.to_period('W') # Group by week
        x_axis_title = 'Week'
        # Generate full week range for the current month
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        full_range = pd.period_range(start=start_of_month, end=end_of_month, freq='W')
    else: # 'all_time' or 'this_year'
        df['period_group'] = df['date_of_purchase'].dt.to_period('M') # Group by month
        x_axis_title = 'Month'
        # Generate full month range
        min_date = df['date_of_purchase'].min()
        max_date = df['date_of_purchase'].max()
        full_range = pd.period_range(start=min_date, end=max_date, freq='M')

    # Check if multiple users are present in the queryset
    multiple_users = receipts_queryset.values('user').distinct().count() > 1

    if multiple_users:
        # Group by period_group and user for stacked bars
        grouped_spending = df.groupby(['period_group', 'user__username'])['total_amount'].sum().unstack(fill_value=0).stack().reset_index(name='total_amount')
        
        # Ensure all periods are present for each user
        all_combinations = pd.MultiIndex.from_product([full_range, grouped_spending['user__username'].unique()], names=['period_group', 'user__username']).to_frame(index=False)
        grouped_spending = pd.merge(all_combinations, grouped_spending, on=['period_group', 'user__username'], how='left').fillna(0)
        grouped_spending['period_group'] = grouped_spending['period_group'].astype(str)
        fig = px.bar(grouped_spending, x='period_group', y='total_amount', color='user__username', title='Spending Over Time by User', barmode='stack', labels={'period_group': x_axis_title, 'total_amount': 'Total Spending'})
    else:
        # Group by period_group only for single bars
        grouped_spending = df.groupby('period_group')['total_amount'].sum().reset_index()
        # Ensure all periods are present
        full_df = pd.DataFrame({'period_group': full_range})
        grouped_spending = pd.merge(full_df, grouped_spending, on='period_group', how='left').fillna(0)
        grouped_spending['period_group'] = grouped_spending['period_group'].astype(str) # Convert Period/Date to string for Plotly
        fig = px.bar(grouped_spending, x='period_group', y='total_amount', title='Spending Over Time', labels={'period_group': x_axis_title, 'total_amount': 'Total Spending'})

    return fig.to_html(full_html=False, include_plotlyjs='cdn')