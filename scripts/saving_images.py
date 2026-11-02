def main():
    parser = argparse.ArgumentParser(
        description="Procesa MRIs del dataset OASIS en batch"
    )
    parser.add_argument(
        "oasis_root",
        help="Ruta raíz de la carpeta OASIS (que contiene disc1, disc2, ...)",
    )
    parser.add_argument(
        "--start", type=int, default=1,
        help="Número del primer disco (default: 1)",
    )
    parser.add_argument(
        "--end", type=int, default=1,
        help="Número del último disco (default: 1)",
    )

    args = parser.parse_args()

    oasis_root = os.path.expanduser(args.oasis_root)
    output_dir = os.path.join(oasis_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"OASIS root: {oasis_root}")
    print(f"Procesando discos: {args.start} a {args.end}")
    print(f"Output: {output_dir}\n")

    # Buscar archivos
    mri_files = find_mri_files(oasis_root, args.start, args.end)

    if not mri_files:
        print("[ERROR] No se encontraron archivos MRI. Verifica la ruta y la estructura de carpetas.")
        return

    print(f"\nTotal de archivos a procesar: {len(mri_files)}\n")

    # Procesar cada archivo
    all_metrics = []
    for i, filepath in enumerate(mri_files, 1):
        subject_id = extract_subject_id(filepath)
        print(f"[{i}/{len(mri_files)}] Procesando {subject_id}...")

        try:
            metrics = process_mri(filepath, output_dir)
            all_metrics.append(metrics)
        except Exception as e:
            print(f"[ERROR] Falló {subject_id}: {e}")

    # Guardar CSV
    csv_path = save_metrics_csv(all_metrics, output_dir)

    print(f"\n{'='*50}")
    print(f"Procesamiento completado")
    print(f"  Imágenes procesadas: {len(all_metrics)}/{len(mri_files)}")
    print(f"  PNGs guardados en:   {output_dir}/")
    print(f"  Métricas en:         {csv_path}")


if __name__ == "__main__":
    main()