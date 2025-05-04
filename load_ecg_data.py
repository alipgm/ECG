import os
import wfdb
import numpy as np

def get_record_names(data_dir):
    """Get all record names (without extensions) from the dataset directory."""
    record_names = []
    for file in os.listdir(data_dir):
        if file.endswith('.dat'):
            record_name = os.path.splitext(file)[0]
            record_names.append(record_name)
    return sorted(set(record_names))

def load_mitbih_record(data_dir, record_name):
    """
    Load a single ECG record and its annotations.
    Returns:
        signal (ndarray), annotation (wfdb.Annotation), metadata (dict)
    """
    record_path = os.path.join(data_dir, record_name)
    record = wfdb.rdrecord(record_path)
    annotation = wfdb.rdann(record_path, 'atr')
    
    metadata = {
        'fs': record.fs,
        'sig_name': record.sig_name,
        'units': record.units,
        'length': record.sig_len
    }

    return record.p_signal, annotation, metadata

def load_all_records(data_dir):
    """
    Load all ECG records from the specified directory.
    Returns:
        dict: key = record name, value = dict(signal, annotation, metadata)
    """
    records = {}
    record_names = get_record_names(data_dir)

    for name in record_names:
        try:
            signal, ann, meta = load_mitbih_record(data_dir, name)
            records[name] = {
                'signal': signal,
                'annotation': ann,
                'metadata': meta
            }
            print(f"Loaded {name}: signal shape {signal.shape}, {len(ann.sample)} annotations")
        except Exception as e:
            print(f"Error loading {name}: {e}")

    return records

if __name__ == "__main__":
    data_path = "/content/drive/MyDrive/mit-db/mitdb"

    all_records = load_all_records(data_path)

    print("\nSummary:")
    print(f"Total records loaded: {len(all_records)}")
    total_beats = sum(len(r['annotation'].sample) for r in all_records.values())
    print(f"Total beats annotated: {total_beats}")

    # Example access
    if "100" in all_records:
        rec = all_records["100"]
        print(f"\nExample Record 100:")
        print(f"Signal shape: {rec['signal'].shape}")
        print(f"Beat types: {set(rec['annotation'].symbol)}")
