import xml.etree.ElementTree as et
import os


# https://docs.aws.amazon.com/mediapackage/latest/ug/dash-trtmts.html
def test_segmenttemplate_is_child_of_representation():
    # load period manifest:
    manifest_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'manifest.xml')
    tree = et.parse('manifest.xml')
    root = tree.getroot()
    # check that root level tag is Period
    assert root.tag == 'Period'

    # check that there's 1 AdaptationSet child element:
    adaptationSet_list = root.findall('AdaptationSet')
    assert len(adaptationSet_list) == 1
    adaptationSet = adaptationSet_list[0]

    # check that there's 1 Representation child element
    representation_list = adaptationSet.findall('Representation')
    assert len(representation_list) == 1
    representation = representation_list[0]

    # check that SegmentTemplate element is child of Representation element:
    segmentTemplate_list = representation.findall('SegmentTemplate')
    # fails here:
    assert len(segmentTemplate_list) > 0

