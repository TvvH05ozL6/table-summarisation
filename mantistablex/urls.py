from django.urls import path

from . import views

urlpatterns = [
    # Index
    path('', views.index, name='index'),

    # Tables
    path('tables/', views.home, name='home'),
    path('tables/newtable/', views.create_tables, name='createTables'),
    path('delete/<int:table_id>/', views.delete_table, name='deleteTable'),
    path('tables/deleteannotation/<int:annotation_id>', views.delete_annotation, name='deleteAnnotation'),
    path('tables/show/newannotation/<int:table_id>', views.add_annotation, name='addAnnotation'),
    path('tables/editannotation/<int:annotation_id>', views.edit_annotation, name='editAnnotation'),

    # TODO: remove?
    path('tables/analyze/<int:table_id>', views.analyze_table, name='analyzeTable'),
    path('load-gs-table/', views.load_gs_tables, name='load_gs_table'),
    path('delete-gs-table/', views.delete_gs_tables, name='delete_gs_table'),

    # Process
    path('process/<int:table_id>', views.show_table, name='showTable'),
    path('process/select-familiarity/<int:table_id>', views.select_familiarity, name='selectFamiliarity'),  # Step 3
    path('process/triples-visualization/<int:table_id>', views.triples_viz, name='triplesViz'),  # Step 4
    path('process/summary/<int:table_id>', views.lexicalisation, name='summary'),

    # Analize with eye tracker
    path('experiments/analyze/<int:table_id>', views.analyze_table, name='analyzeTable'),
    path('experiments/<int:table_id>/eye-tracking', views.eye_tracking_table, name='eyeTracking'),  # Step 1
    path('experiments/<int:table_id>/questionnaires', views.questionnaires, name='questionnaires'),  # Step 2

    path('export', views.export, name='export'),
]
