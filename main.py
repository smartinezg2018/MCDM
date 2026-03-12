import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. CONFIGURACIÓN DE ESTILO (Inspirado en publicaciones científicas)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'figure.dpi': 100})
color_palette = sns.color_palette("viridis", as_cmap=False)

# 2. CARGA Y LIMPIEZA DE DATOS
file_path = 'systematic mapping MCDM Scopus - revisión (1).csv'
df = pd.read_csv(file_path)

# Limpieza de nombres de columnas y tipos de datos
df.columns = df.columns.str.strip()
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Numero variables'] = pd.to_numeric(df['Numero variables'], errors='coerce')
df = df.dropna(subset=['Year']) # Eliminar filas sin año para el análisis temporal

# 3. CREACIÓN DEL DASHBOARD DE REVISIÓN SISTEMÁTICA
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Systematic Mapping: MCDM in Renewable Energy Site Selection\n(Methodology: Quesada-Bedoya et al., 2025)', fontsize=18, fontweight='bold')

# --- SUBPLOT 1: Evolución Temporal (RQ1) ---
ax1 = plt.subplot(2, 2, 1)
yearly_dist = df.groupby('Year').size()
sns.lineplot(x=yearly_dist.index, y=yearly_dist.values, marker='o', color='teal', linewidth=2.5, ax=ax1)
ax1.fill_between(yearly_dist.index, yearly_dist.values, color='teal', alpha=0.1)
ax1.set_title('RQ1: Scientific Production Trend', fontsize=13, loc='left')
ax1.set_ylabel('Number of Publications')
ax1.set_xlabel('Year')

# --- SUBPLOT 2: Métodos MCDM Prevalentes (RQ2) ---
ax2 = plt.subplot(2, 2, 2)
# Limpiamos y contamos métodos (tomando los top 8)
mcdm_counts = df['MCDM method'].str.split(',').explode().str.strip().value_counts().head(8)
sns.barplot(x=mcdm_counts.values, y=mcdm_counts.index, palette='magma', ax=ax2)
ax2.set_title('RQ2: Top MCDM Methods Identified', fontsize=13, loc='left')
ax2.set_xlabel('Frequency')

# --- SUBPLOT 3: Tipo de Energía y Entorno (RQ3) ---
ax3 = plt.subplot(2, 2, 3)
energy_env = df.groupby(['Solar/Eolico', 'onshore/offshore']).size().unstack().fillna(0)
energy_env.plot(kind='bar', stacked=True, ax=ax3, color=['#34495e', '#3498db'])
ax3.set_title('RQ3: Energy Type vs Environment', fontsize=13, loc='left')
ax3.set_ylabel('Count')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
ax3.legend(title='Context')

# --- SUBPLOT 4: Complejidad del Modelo - Variables (RQ5) ---
ax4 = plt.subplot(2, 2, 4)
sns.boxplot(x='Solar/Eolico', y='Numero variables', data=df, palette='Set2', ax=ax4)
sns.stripplot(x='Solar/Eolico', y='Numero variables', data=df, color=".3", size=4, alpha=0.5, ax=ax4)
ax4.set_title('RQ5: Model Complexity (No. of Variables)', fontsize=13, loc='left')
ax4.set_ylabel('Variables Count')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 4. TABLA DE SÍNTESIS FINAL (Equivalente a Table 21 del PDF)
print("\n" + "="*50)
print("SUMMARY TABLE: KEY REVIEWS (TOP CITED/RECENT)")
print("="*50)

# Seleccionamos columnas clave y formateamos para visualización
summary_table = df[['Authors', 'Year', 'MCDM method', 'país', 'Numero variables', 'onshore/offshore']].head(15)
summary_table = summary_table.sort_values(by='Year', ascending=False)

# Mostrar tabla formateada en el notebook
from IPython.display import display
display(summary_table)

# 5. EXPORTACIÓN DE RESULTADOS
# summary_table.to_csv('Systematic_Mapping_Results.csv', index=False)