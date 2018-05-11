from __future__ import print_function
import csv,datetime,dateutil


def parse_endpoints(fn):

    rdr = csv.reader(file(fn))
    top=next(rdr)
    sections = []
    for r in rdr:
        print(repr(r))
        d1 = dateutil.parser.parse(r[2])
        print("  ", d1)
        d2 = dateutil.parser.parse(r[3])
        print("  ", d2)
        print("  relative ", d2-d1)
        delta=d2-d1
        print("delta.seconds:", delta.seconds, "microseconds", delta.microseconds)
        newrow = [r[0], int(r[1]), d1, d2]
        sections.append(newrow)

    # use the earliest time we have for the start time
    starttime = sections[0][2]
    dsections = []
    for row in sections:
        t1 = row[2]-starttime
        row.append(t1.seconds) # add the start time of the section in seconds since beginning
        t2 = row[3]-starttime
        row.append(t2.seconds)
        delta = t2-t1 # delta.seconds, delta.microseconds]
        row.append(delta.seconds)
        row.append(delta.microseconds)
        print(row)
        dsections.append(dict(description=row[0], channel_number=row[1], start_section_dtime=row[2],end_section_dtime=row[3], start_time_sec=row[4], end_time_sec=row[5], duration_sec=row[6],
                         duration_microsec=row[7]))

    return sections, dsections

    #hdr = dict()
    #hdr['file_name'] = fn
    #hdr['start_time'] = starttime
    #hdr['start_date'] = 
    
def test_read_endpoints():
    fn = 'chrisEndpointsExtractedTable.csv'


def write_simple_timepoint_file(fn, dtimes):
    wtr = csv.writer(file(fn,"w"))
    for dd in dtimes:
        #print dd
        #print '--------'
        row = [dd['description'], dd['start_time_sec'], dd['end_time_sec'], dd['duration_sec'] ]
        print(row)
        wtr.writerow(row)
